"""Disassemble a bounded virtual-address range from a local x64 PE file."""

from __future__ import annotations

import argparse
from pathlib import Path

import pefile
from capstone import CS_ARCH_X86, CS_MODE_64, Cs


parser = argparse.ArgumentParser()
parser.add_argument("binary", type=Path)
parser.add_argument("address", type=lambda value: int(value, 0))
parser.add_argument("length", type=lambda value: int(value, 0), nargs="?", default=256)
args = parser.parse_args()
if args.length < 1 or args.length > 1024 * 1024:
    raise SystemExit("Length must be between 1 byte and 1 MiB.")

pe = pefile.PE(str(args.binary), fast_load=True)
base = pe.OPTIONAL_HEADER.ImageBase
rva = args.address - base if args.address >= base else args.address
file_offset = pe.get_offset_from_rva(rva)
with args.binary.open("rb") as stream:
    stream.seek(file_offset)
    data = stream.read(args.length)

decoder = Cs(CS_ARCH_X86, CS_MODE_64)
for instruction in decoder.disasm(data, base + rva):
    raw = instruction.bytes.hex(" ")
    print(f"0x{instruction.address:X}  {raw:<45} {instruction.mnemonic:<9} {instruction.op_str}")
