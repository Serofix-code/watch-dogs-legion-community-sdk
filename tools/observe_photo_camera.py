"""Read-only runtime observer for the mapped photo-camera manager interface.

The tool opens WatchDogsLegion.exe with query/read access only. It never
allocates, injects, hooks, suspends threads, changes protection, or writes.
Offsets apply only to the exact fingerprinted Steam DX11 module.
"""

from __future__ import annotations

import argparse
import ctypes
from ctypes import wintypes
import hashlib
import json
import math
from pathlib import Path
import struct
import sys
import time


PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
PROCESS_VM_READ = 0x0010
TH32CS_SNAPPROCESS = 0x00000002
TH32CS_SNAPMODULE = 0x00000008
TH32CS_SNAPMODULE32 = 0x00000010
INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
MEM_COMMIT = 0x1000
MEM_PRIVATE = 0x20000
PAGE_GUARD = 0x100
PAGE_NOACCESS = 0x01

EXPECTED_SHA256 = "086968CD9EC4D5939248846EAFA2DA72210FDDEB1164E79CBD08164313A0086E"
MODULE_NAME = "DuniaDemo_clang_64_dx11.dll"
MANAGER_INTERFACE_GLOBAL_RVA = 0xB486020
MANAGER_INTERFACE_VTABLE_RVA = 0xA116C00
FREE_PHOTO_COMPONENT_VTABLE_RVA = 0xA0FC380
PHOTO_CAMERA_HELPER_VTABLE_RVA = 0xA116FC0


class PROCESSENTRY32W(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD), ("cntUsage", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD), ("th32DefaultHeapID", ctypes.c_size_t),
        ("th32ModuleID", wintypes.DWORD), ("cntThreads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD), ("pcPriClassBase", wintypes.LONG),
        ("dwFlags", wintypes.DWORD), ("szExeFile", wintypes.WCHAR * 260),
    ]


class MODULEENTRY32W(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD), ("th32ModuleID", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD), ("GlblcntUsage", wintypes.DWORD),
        ("ProccntUsage", wintypes.DWORD), ("modBaseAddr", ctypes.POINTER(ctypes.c_byte)),
        ("modBaseSize", wintypes.DWORD), ("hModule", wintypes.HMODULE),
        ("szModule", wintypes.WCHAR * 256), ("szExePath", wintypes.WCHAR * 260),
    ]


class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", ctypes.c_void_p), ("AllocationBase", ctypes.c_void_p),
        ("AllocationProtect", wintypes.DWORD), ("PartitionId", wintypes.WORD),
        ("_alignment", wintypes.WORD), ("RegionSize", ctypes.c_size_t),
        ("State", wintypes.DWORD), ("Protect", wintypes.DWORD),
        ("Type", wintypes.DWORD), ("_alignment2", wintypes.DWORD),
    ]


kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
kernel32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
kernel32.Process32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
kernel32.Process32FirstW.restype = wintypes.BOOL
kernel32.Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
kernel32.Process32NextW.restype = wintypes.BOOL
kernel32.Module32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(MODULEENTRY32W)]
kernel32.Module32FirstW.restype = wintypes.BOOL
kernel32.Module32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(MODULEENTRY32W)]
kernel32.Module32NextW.restype = wintypes.BOOL
kernel32.OpenProcess.restype = wintypes.HANDLE
kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
kernel32.VirtualQueryEx.restype = ctypes.c_size_t
kernel32.VirtualQueryEx.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.POINTER(MEMORY_BASIC_INFORMATION), ctypes.c_size_t]
kernel32.ReadProcessMemory.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
kernel32.ReadProcessMemory.restype = wintypes.BOOL
kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
kernel32.CloseHandle.restype = wintypes.BOOL


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--process", default="WatchDogsLegion.exe")
    parser.add_argument("--watch", action="store_true", help="Poll until interrupted.")
    parser.add_argument("--interval", type=float, default=0.5)
    parser.add_argument("--skip-hash", action="store_true", help="Allow an unverified module build.")
    parser.add_argument("--json", action="store_true", help="Print one JSON object per sample.")
    parser.add_argument(
        "--scan-components", action="store_true",
        help="Scan readable private memory once for engine-owned free-photo component candidates.",
    )
    parser.add_argument(
        "--max-scan-mib", type=int, default=4096,
        help="Maximum readable private memory inspected by --scan-components (default: 4096).",
    )
    parser.add_argument("--max-components", type=int, default=32)
    return parser.parse_args()


def close(handle: int | None) -> None:
    if handle and handle != INVALID_HANDLE_VALUE:
        kernel32.CloseHandle(handle)


def find_process(name: str) -> int | None:
    snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if snapshot == INVALID_HANDLE_VALUE:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        entry = PROCESSENTRY32W()
        entry.dwSize = ctypes.sizeof(entry)
        if not kernel32.Process32FirstW(snapshot, ctypes.byref(entry)):
            raise ctypes.WinError(ctypes.get_last_error())
        while True:
            if entry.szExeFile.casefold() == name.casefold():
                return int(entry.th32ProcessID)
            if not kernel32.Process32NextW(snapshot, ctypes.byref(entry)):
                return None
    finally:
        close(snapshot)


def find_module(pid: int, name: str) -> tuple[int, int, Path] | None:
    snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, pid)
    if snapshot == INVALID_HANDLE_VALUE:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        entry = MODULEENTRY32W()
        entry.dwSize = ctypes.sizeof(entry)
        if not kernel32.Module32FirstW(snapshot, ctypes.byref(entry)):
            raise ctypes.WinError(ctypes.get_last_error())
        while True:
            if entry.szModule.casefold() == name.casefold():
                base = ctypes.cast(entry.modBaseAddr, ctypes.c_void_p).value
                if base is None:
                    return None
                return int(base), int(entry.modBaseSize), Path(entry.szExePath)
            if not kernel32.Module32NextW(snapshot, ctypes.byref(entry)):
                return None
    finally:
        close(snapshot)


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest().upper()


class Reader:
    def __init__(self, pid: int):
        self.handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION | PROCESS_VM_READ, False, pid)
        if not self.handle:
            raise ctypes.WinError(ctypes.get_last_error())

    def close(self) -> None:
        close(self.handle)
        self.handle = None

    def readable(self, address: int, length: int) -> bool:
        if address < 0x10000 or length < 1:
            return False
        info = MEMORY_BASIC_INFORMATION()
        if not kernel32.VirtualQueryEx(self.handle, ctypes.c_void_p(address), ctypes.byref(info), ctypes.sizeof(info)):
            return False
        start = int(info.BaseAddress or 0)
        end = start + int(info.RegionSize)
        return (info.State == MEM_COMMIT and start <= address and address + length <= end
                and not info.Protect & (PAGE_GUARD | PAGE_NOACCESS))

    def read(self, address: int, length: int) -> bytes:
        if not self.readable(address, length):
            raise ValueError(f"unreadable range 0x{address:X} (+0x{length:X})")
        buffer = ctypes.create_string_buffer(length)
        read = ctypes.c_size_t()
        if not kernel32.ReadProcessMemory(self.handle, ctypes.c_void_p(address), buffer, length, ctypes.byref(read)) or read.value != length:
            raise ctypes.WinError(ctypes.get_last_error())
        return buffer.raw

    def u8(self, address: int) -> int:
        return self.read(address, 1)[0]

    def u64(self, address: int) -> int:
        return struct.unpack("<Q", self.read(address, 8))[0]

    def regions(self):
        address = 0
        while True:
            info = MEMORY_BASIC_INFORMATION()
            queried = kernel32.VirtualQueryEx(
                self.handle, ctypes.c_void_p(address), ctypes.byref(info), ctypes.sizeof(info)
            )
            if not queried:
                return
            base = int(info.BaseAddress or 0)
            size = int(info.RegionSize)
            if size <= 0:
                return
            yield base, size, int(info.State), int(info.Protect), int(info.Type)
            next_address = base + size
            if next_address <= address:
                return
            address = next_address


def finite_vector(values: tuple[float, ...]) -> bool:
    return all(math.isfinite(value) and abs(value) < 1.0e9 for value in values)


def read_component(reader: Reader, address: int, expected_vtable: int) -> dict[str, object] | None:
    if not reader.readable(address, 0x2A0):
        return None
    raw = reader.read(address, 0x2A0)
    if struct.unpack_from("<Q", raw)[0] != expected_vtable:
        return None
    orientation = struct.unpack_from("<3f", raw, 0x70)
    position_xyz = struct.unpack_from("<3f", raw, 0x194)
    limits = struct.unpack_from("<2f", raw, 0x1C8)
    scalars = (
        struct.unpack_from("<f", raw, 0x188)[0],
        struct.unpack_from("<f", raw, 0x18C)[0],
        struct.unpack_from("<f", raw, 0x1F4)[0],
    )
    if not finite_vector(orientation + position_xyz + limits + scalars):
        return None
    return {
        "address": f"0x{address:X}",
        "orientation": list(orientation),
        "position": list(position_xyz),
        "maxDistanceFromPlayer": scalars[0],
        "cameraMoveSpeed": scalars[1],
        "minimumPitch": limits[0],
        "maximumPitch": limits[1],
        "orbitMovementSpeed": scalars[2],
        "backendHandle": f"0x{struct.unpack_from('<Q', raw, 0x280)[0]:X}",
    }


def read_helper(reader: Reader, address: int, expected_vtable: int) -> dict[str, object] | None:
    """Read the engine-owned 0x160-byte PhotoCameraManager runtime helper."""
    if not address or not reader.readable(address, 0x160):
        return None
    raw = reader.read(address, 0x160)
    vtable = struct.unpack_from("<Q", raw)[0]
    if vtable != expected_vtable:
        return {
            "address": f"0x{address:X}",
            "vtable": f"0x{vtable:X}",
            "expectedVtable": f"0x{expected_vtable:X}",
            "valid": False,
        }
    return {
        "address": f"0x{address:X}",
        "vtable": f"0x{vtable:X}",
        "valid": True,
        "inputService": f"0x{struct.unpack_from('<Q', raw, 0x20)[0]:X}",
        "cameraContext": f"0x{struct.unpack_from('<Q', raw, 0x28)[0]:X}",
        "selectedMode": raw[0x38],
        "primaryTransitionToken": struct.unpack_from("<I", raw, 0xC8)[0],
        "eventSubscription": f"0x{struct.unpack_from('<Q', raw, 0xD0)[0]:X}",
        "modeRegistrationEnabled": bool(raw[0x120]),
        "secondaryTransitionToken": struct.unpack_from("<I", raw, 0x14C)[0],
        "freeModeTransitionToken": struct.unpack_from("<I", raw, 0x154)[0],
    }


def scan_components(
    reader: Reader, module_base: int, max_scan_bytes: int, max_results: int
) -> tuple[list[dict[str, object]], int, bool]:
    """Locate exact component-vtable pointers without mutating the target process."""
    needle = struct.pack("<Q", module_base + FREE_PHOTO_COMPONENT_VTABLE_RVA)
    candidates: list[dict[str, object]] = []
    seen: set[int] = set()
    scanned = 0
    reached_limit = False
    chunk_size = 4 * 1024 * 1024

    for base, size, state, protect, memory_type in reader.regions():
        if state != MEM_COMMIT or memory_type != MEM_PRIVATE:
            continue
        if protect & (PAGE_GUARD | PAGE_NOACCESS):
            continue
        offset = 0
        carry = b""
        while offset < size:
            remaining_budget = max_scan_bytes - scanned
            if remaining_budget <= 0:
                reached_limit = True
                return candidates, scanned, reached_limit
            length = min(chunk_size, size - offset, remaining_budget)
            chunk_address = base + offset
            try:
                block = reader.read(chunk_address, length)
            except (OSError, ValueError):
                carry = b""
                offset += length
                continue
            scanned += length
            searchable = carry + block
            searchable_base = chunk_address - len(carry)
            position = searchable.find(needle)
            while position >= 0:
                address = searchable_base + position
                if address % 8 == 0 and address not in seen:
                    seen.add(address)
                    candidate = read_component(reader, address, module_base + FREE_PHOTO_COMPONENT_VTABLE_RVA)
                    if candidate is not None:
                        candidates.append(candidate)
                        if len(candidates) >= max_results:
                            return candidates, scanned, reached_limit
                position = searchable.find(needle, position + 1)
            carry = searchable[-(len(needle) - 1):]
            offset += length
    return candidates, scanned, reached_limit


def sample(reader: Reader, pid: int, module_base: int) -> dict[str, object]:
    global_address = module_base + MANAGER_INTERFACE_GLOBAL_RVA
    interface = reader.u64(global_address)
    result: dict[str, object] = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "pid": pid,
        "moduleBase": f"0x{module_base:X}", "globalAddress": f"0x{global_address:X}",
        "interface": f"0x{interface:X}", "valid": False,
    }
    if not interface or not reader.readable(interface, 0x320):
        result["reason"] = "manager interface is null or unreadable"
        return result
    vtable = reader.u64(interface)
    helper = reader.u64(interface + 0x318)
    result.update({
        "vtable": f"0x{vtable:X}",
        "expectedVtable": f"0x{module_base + MANAGER_INTERFACE_VTABLE_RVA:X}",
        "freeModeState": bool(reader.u8(interface + 0x100)),
        "requestedState": bool(reader.u8(interface + 0x101)),
        "activeState": bool(reader.u8(interface + 0x102)),
        "helper": f"0x{helper:X}",
    })
    result["valid"] = vtable == module_base + MANAGER_INTERFACE_VTABLE_RVA
    if not result["valid"]:
        result["reason"] = "unexpected interface vtable"
    elif helper:
        result["helperState"] = read_helper(
            reader, helper, module_base + PHOTO_CAMERA_HELPER_VTABLE_RVA
        )
    return result


def main() -> int:
    if sys.platform != "win32":
        raise SystemExit("This observer requires Windows.")
    args = arguments()
    if args.interval < 0.05:
        raise SystemExit("--interval must be at least 0.05 seconds.")
    if args.max_scan_mib < 1:
        raise SystemExit("--max-scan-mib must be positive.")
    if args.max_components < 1 or args.max_components > 256:
        raise SystemExit("--max-components must be between 1 and 256.")
    pid = find_process(args.process)
    if pid is None:
        print(f"{args.process} is not running.", file=sys.stderr)
        return 2
    module = find_module(pid, MODULE_NAME)
    if module is None:
        print(f"{MODULE_NAME} is not loaded in PID {pid}.", file=sys.stderr)
        return 3
    module_base, _, module_path = module
    if not args.skip_hash:
        actual = digest(module_path)
        if actual != EXPECTED_SHA256:
            print(f"Unsupported module SHA-256: {actual}", file=sys.stderr)
            return 4

    reader = Reader(pid)
    try:
        components = None
        scan_metadata = None
        if args.scan_components:
            components, scanned, reached_limit = scan_components(
                reader, module_base, args.max_scan_mib * 1024 * 1024, args.max_components
            )
            scan_metadata = {
                "bytesScanned": scanned,
                "reachedByteLimit": reached_limit,
                "candidateCount": len(components),
            }
        while True:
            current = sample(reader, pid, module_base)
            if components is not None:
                components = [
                    refreshed
                    for component in components
                    if (refreshed := read_component(
                        reader,
                        int(str(component["address"]), 16),
                        module_base + FREE_PHOTO_COMPONENT_VTABLE_RVA,
                    )) is not None
                ]
                current["componentScan"] = {
                    **scan_metadata,
                    "activeCandidateCount": len(components),
                }
                current["componentCandidates"] = components
            if args.json:
                print(json.dumps(current, sort_keys=True), flush=True)
            else:
                print(" | ".join(f"{key}={value}" for key, value in current.items()), flush=True)
            if not args.watch:
                return 0 if current["valid"] else 5
            time.sleep(args.interval)
    except KeyboardInterrupt:
        return 130
    finally:
        reader.close()


if __name__ == "__main__":
    raise SystemExit(main())
