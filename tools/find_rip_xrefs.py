"""Find x64 RIP-relative references to one or more virtual addresses in a PE.

This is a read-only research helper. Targets may be written as hexadecimal
virtual addresses (``0x18B33C7D8``) or as image-relative RVAs prefixed with
``rva:`` (``rva:0xB33C7D8``). Only bounded instruction context is printed.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pefile
from capstone import CS_ARCH_X86, CS_MODE_64, Cs
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("binary", type=Path)
    parser.add_argument("targets", nargs="+")
    parser.add_argument("--max-results", type=int, default=200)
    parser.add_argument("--section", action="append", default=[])
    parser.add_argument("--include-relative-branches", action="store_true")
    return parser.parse_args()


def parse_target(value: str, image_base: int) -> int:
    if value.lower().startswith("rva:"):
        return image_base + int(value[4:], 0)
    return int(value, 0)


def displacement_candidates(code: bytes, va: int, targets: set[int], chunk_size: int = 8 * 1024 * 1024):
    """Vector-scan every possible signed disp32 field in bounded chunks."""
    wanted = np.array(sorted(targets), dtype=np.int64)
    for base in range(0, len(code), chunk_size):
        end = min(len(code), base + chunk_size + 3)
        chunk = memoryview(code)[base:end]
        for alignment in range(4):
            count = (len(chunk) - alignment) // 4
            if count <= 0:
                continue
            displacements = np.frombuffer(chunk, dtype="<i4", count=count, offset=alignment)
            positions = base + alignment + np.arange(count, dtype=np.int64) * 4
            destinations = displacements.astype(np.int64) + va + positions + 4
            for index in np.flatnonzero(np.isin(destinations, wanted)):
                yield int(positions[index])


def validate_candidate(
    decoder: Cs,
    code: bytes,
    va: int,
    displacement: int,
    targets: set[int],
    include_relative_branches: bool,
):
    """Resolve a raw disp32 candidate back to a plausible RIP-relative instruction."""
    hits: list[tuple[object, set[int]]] = []
    for start in range(max(0, displacement - 14), displacement + 1):
        for instruction in decoder.disasm(code[start:min(len(code), displacement + 20)], va + start):
            relative_start = instruction.address - va
            relative_end = relative_start + instruction.size
            if not (relative_start <= displacement and displacement + 4 <= relative_end):
                if relative_start > displacement:
                    break
                continue
            if instruction.id == 0:
                continue
            destinations = {
                instruction.address + instruction.size + operand.mem.disp
                for operand in instruction.operands
                if operand.type == X86_OP_MEM and operand.mem.base == X86_REG_RIP
            }
            if include_relative_branches and instruction.mnemonic in {"call", "jmp"}:
                destinations.update(
                    operand.imm for operand in instruction.operands if operand.type == X86_OP_IMM
                )
            if destinations & targets:
                hits.append((instruction, destinations & targets))

    # Starting the decoder one byte into a REX-prefixed instruction can produce
    # a second, plausible 32-bit decoding with the same displacement. Prefer the
    # earliest instruction whose byte span contains the later alternative.
    accepted: list[tuple[object, set[int]]] = []
    for instruction, matches in sorted(hits, key=lambda item: (item[0].address, -item[0].size)):
        start = instruction.address
        end = start + instruction.size
        if any(existing.address <= start and end <= existing.address + existing.size for existing, _ in accepted):
            continue
        if any(existing.address == start for existing, _ in accepted):
            continue
        accepted.append((instruction, matches))
    yield from accepted


def main() -> int:
    args = arguments()
    pe = pefile.PE(str(args.binary), fast_load=True)
    image_base = pe.OPTIONAL_HEADER.ImageBase
    targets = {parse_target(value, image_base) for value in args.targets}
    decoder = Cs(CS_ARCH_X86, CS_MODE_64)
    decoder.detail = True
    decoder.skipdata = True
    count = 0

    for section in pe.sections:
        if not section.IMAGE_SCN_MEM_EXECUTE:
            continue
        section_name = section.Name.rstrip(b"\0").decode("ascii", "replace")
        if args.section and section_name not in args.section:
            continue
        code = section.get_data()
        va = image_base + section.VirtualAddress
        reported: set[tuple[int, int]] = set()
        for displacement in displacement_candidates(code, va, targets):
            for instruction, matches in validate_candidate(
                decoder, code, va, displacement, targets, args.include_relative_branches
            ):
                for destination in sorted(matches):
                    key = (instruction.address, destination)
                    if key in reported:
                        continue
                    reported.add(key)
                    try:
                        file_offset = pe.get_offset_from_rva(destination - image_base)
                        target_label = f"VA=0x{destination:X} file=0x{file_offset:X}"
                    except pefile.PEFormatError:
                        target_label = f"VA=0x{destination:X} (not file-backed)"
                    print(f"\nTarget {target_label}; reference in {section_name}")
                    print(f"> 0x{instruction.address:X}: {instruction.mnemonic:<8} {instruction.op_str}")
                    count += 1
                    if count >= args.max_results:
                        return 0

    if not count:
        print("No RIP-relative executable references found.")
        return 2
    print(f"\nFound {count} reference(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
