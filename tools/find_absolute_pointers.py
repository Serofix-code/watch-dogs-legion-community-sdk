"""Find exact little-endian absolute pointer values in a local PE file."""

from __future__ import annotations

import argparse
import mmap
from pathlib import Path
import struct

import pefile


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("binary", type=Path)
    parser.add_argument("targets", nargs="+", help="VA or rva:0x... values")
    parser.add_argument("--max-results", type=int, default=100)
    parser.add_argument(
        "--include-rva32",
        action="store_true",
        help="also find exact 32-bit image-relative values",
    )
    return parser.parse_args()


def main() -> int:
    args = arguments()
    pe = pefile.PE(str(args.binary), fast_load=True)
    image_base = pe.OPTIONAL_HEADER.ImageBase
    targets = []
    for text in args.targets:
        value = image_base + int(text[4:], 0) if text.lower().startswith("rva:") else int(text, 0)
        targets.append(value)

    count = 0
    with args.binary.open("rb") as stream, mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ) as data:
        for target in targets:
            patterns = [("VA64", struct.pack("<Q", target))]
            target_rva = target - image_base
            if args.include_rva32 and 0 <= target_rva <= 0xFFFFFFFF:
                patterns.append(("RVA32", struct.pack("<I", target_rva)))
            for encoding, needle in patterns:
                cursor = 0
                while count < args.max_results:
                    offset = data.find(needle, cursor)
                    if offset < 0:
                        break
                    cursor = offset + 1
                    try:
                        rva = pe.get_rva_from_offset(offset)
                        location = f"RVA=0x{rva:X} VA=0x{image_base + rva:X}"
                    except pefile.PEFormatError:
                        location = "not mapped to an image RVA"
                    print(
                        f"target=0x{target:X} encoding={encoding} "
                        f"file=0x{offset:X} {location}"
                    )
                    count += 1

    if not count:
        print("No exact absolute pointer values found.")
        return 2
    print(f"Found {count} pointer occurrence(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
