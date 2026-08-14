"""Display a small bounded hexadecimal range from a local file."""

from __future__ import annotations

import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("file", type=Path)
parser.add_argument("offset", type=lambda value: int(value, 0))
parser.add_argument("length", type=lambda value: int(value, 0), nargs="?", default=256)
args = parser.parse_args()
if args.length < 1 or args.length > 65536:
    raise SystemExit("Length must be between 1 and 65536 bytes.")
with args.file.open("rb") as stream:
    stream.seek(args.offset)
    data = stream.read(args.length)
for index in range(0, len(data), 16):
    chunk = data[index:index + 16]
    hexadecimal = chunk.hex(" ")
    printable = "".join(chr(value) if 32 <= value < 127 else "." for value in chunk)
    print(f"{args.offset + index:010X}  {hexadecimal:<47}  {printable}")
