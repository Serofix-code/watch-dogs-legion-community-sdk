"""Display a small bounded hexadecimal range from a local file."""

from __future__ import annotations

import argparse
from pathlib import Path

import pefile

parser = argparse.ArgumentParser()
parser.add_argument("file", type=Path)
parser.add_argument("offset", type=lambda value: int(value, 0))
parser.add_argument("length", type=lambda value: int(value, 0), nargs="?", default=256)
parser.add_argument("--pe-address", action="store_true", help="treat offset as a PE VA or RVA")
args = parser.parse_args()
if args.length < 1 or args.length > 65536:
    raise SystemExit("Length must be between 1 and 65536 bytes.")
display_base = args.offset
file_offset = args.offset
if args.pe_address:
    pe = pefile.PE(str(args.file), fast_load=True)
    rva = args.offset - pe.OPTIONAL_HEADER.ImageBase if args.offset >= pe.OPTIONAL_HEADER.ImageBase else args.offset
    file_offset = pe.get_offset_from_rva(rva)
with args.file.open("rb") as stream:
    stream.seek(file_offset)
    data = stream.read(args.length)
for index in range(0, len(data), 16):
    chunk = data[index:index + 16]
    hexadecimal = chunk.hex(" ")
    printable = "".join(chr(value) if 32 <= value < 127 else "." for value in chunk)
    print(f"{display_base + index:010X}  {hexadecimal:<47}  {printable}")
