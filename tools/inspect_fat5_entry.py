"""Inspect one named WDL FAT5 entry without writing extracted game content."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import struct


def compute_name_hash(value: str) -> int:
    result = 0xCBF29CE484222325
    for character in value.lower():
        result = ((result * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF) ^ ord(character)
    return (result & 0x1FFFFFFFFFFFFFFF) | 0xA000000000000000


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fat", type=Path)
    parser.add_argument("name", help="known archive-relative entry name")
    parser.add_argument("--decode", action="store_true", help="decode supported content in memory")
    parser.add_argument("--contains", action="append", default=[], help="print matching ASCII strings")
    parser.add_argument("--max-results", type=int, default=50)
    return parser.parse_args()


def find_entry(fat: Path, target: int) -> tuple[dict[str, int], dict[str, int]]:
    with fat.open("rb") as stream:
        header = stream.read(24)
        if len(header) != 24:
            raise ValueError("truncated FAT5 header")
        magic, version, flags, archive_hash, dependency_count = struct.unpack("<IIIQI", header)
        if magic != 0x46415435 or version != 13:
            raise ValueError("only little-endian WDL FAT5 version 13 is supported")
        stream.seek(16 * dependency_count, 1)
        entry_count_bytes = stream.read(4)
        if len(entry_count_bytes) != 4:
            raise ValueError("truncated FAT5 entry count")
        entry_count = struct.unpack("<I", entry_count_bytes)[0]
        for _ in range(entry_count):
            raw = stream.read(20)
            if len(raw) != 20:
                raise ValueError("truncated FAT5 entry table")
            name_hash, packed_size, offset_high, packed_uncompressed = struct.unpack("<QIII", raw)
            if name_hash != target:
                continue
            entry = {
                "nameHash": name_hash,
                "offset": (offset_high << 2) | (packed_size >> 30),
                "compressedSize": packed_size & 0x3FFFFFFF,
                "uncompressedSize": packed_uncompressed >> 2,
                "compressionScheme": packed_uncompressed & 3,
            }
            return {"version": version, "flags": flags, "archiveHash": archive_hash,
                    "dependencyCount": dependency_count, "entryCount": entry_count}, entry
    raise KeyError(f"entry hash 0x{target:016X} was not found")


def decode(entry: dict[str, int], blob: bytes) -> bytes:
    if entry["compressionScheme"] == 0:
        result = blob
    elif entry["compressionScheme"] == 3:
        try:
            import lz4.block
        except ImportError as error:
            raise RuntimeError("scheme 3 requires: python -m pip install lz4") from error
        if not blob:
            raise ValueError("empty scheme-3 entry")
        result = lz4.block.decompress(blob[1:], uncompressed_size=entry["uncompressedSize"])
    else:
        raise NotImplementedError(f"compression scheme {entry['compressionScheme']} is not supported")
    if len(result) != entry["uncompressedSize"]:
        raise ValueError("decoded size mismatch")
    return result


def main() -> int:
    args = arguments()
    if args.max_results < 1 or args.max_results > 1000:
        raise SystemExit("--max-results must be between 1 and 1000")
    target = compute_name_hash(args.name)
    header, entry = find_entry(args.fat, target)
    print(" ".join(f"{key}={value if key in {'version', 'dependencyCount', 'entryCount'} else f'0x{value:X}'}"
                   for key, value in header.items()))
    print(" ".join(f"{key}={value if key == 'compressionScheme' else f'0x{value:X}'}"
                   for key, value in entry.items()))
    if not args.decode:
        return 0

    dat = args.fat.with_suffix(".dat")
    with dat.open("rb") as stream:
        stream.seek(entry["offset"])
        blob = stream.read(entry["compressedSize"])
    if len(blob) != entry["compressedSize"]:
        raise ValueError("truncated DAT entry")
    decoded = decode(entry, blob)
    print(f"decodedSize=0x{len(decoded):X} sha256={hashlib.sha256(decoded).hexdigest().upper()}")
    if args.contains:
        filters = [value.casefold() for value in args.contains]
        count = 0
        for match in re.finditer(rb"[\x20-\x7E]{4,}", decoded):
            value = match.group().decode("ascii")
            if not any(filter_value in value.casefold() for filter_value in filters):
                continue
            print(f"decodedOffset=0x{match.start():X} {value}")
            count += 1
            if count >= args.max_results:
                break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
