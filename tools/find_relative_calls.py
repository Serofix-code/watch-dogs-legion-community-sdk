"""Find direct x64 call sites targeting a virtual address in a local PE file."""

from __future__ import annotations

import argparse
from pathlib import Path

import pefile
from capstone import CS_ARCH_X86, CS_MODE_64, CS_OP_IMM, Cs


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("binary", type=Path)
    parser.add_argument("target", type=lambda value: int(value, 0), help="target VA or RVA")
    parser.add_argument("--rva-start", type=lambda value: int(value, 0))
    parser.add_argument("--rva-end", type=lambda value: int(value, 0))
    parser.add_argument("--max-results", type=int, default=100)
    return parser.parse_args()


def main() -> int:
    args = arguments()
    pe = pefile.PE(str(args.binary), fast_load=True)
    image_base = pe.OPTIONAL_HEADER.ImageBase
    target = args.target if args.target >= image_base else image_base + args.target
    decoder = Cs(CS_ARCH_X86, CS_MODE_64)
    decoder.detail = True
    count = 0

    with args.binary.open("rb") as stream:
        for section in pe.sections:
            if not section.Characteristics & 0x20000000:  # IMAGE_SCN_MEM_EXECUTE
                continue
            section_rva = section.VirtualAddress
            start_rva = max(section_rva, args.rva_start or section_rva)
            end_rva = min(
                section_rva + section.Misc_VirtualSize,
                args.rva_end or section_rva + section.Misc_VirtualSize,
            )
            if start_rva >= end_rva:
                continue
            file_offset = section.PointerToRawData + (start_rva - section_rva)
            stream.seek(file_offset)
            data = stream.read(end_rva - start_rva)
            for instruction in decoder.disasm(data, image_base + start_rva):
                if instruction.mnemonic != "call" or len(instruction.operands) != 1:
                    continue
                operand = instruction.operands[0]
                if operand.type != CS_OP_IMM or operand.imm != target:
                    continue
                raw = instruction.bytes.hex(" ")
                rva = instruction.address - image_base
                print(f"RVA=0x{rva:X} VA=0x{instruction.address:X} bytes={raw}")
                count += 1
                if count >= args.max_results:
                    print(f"Stopped at --max-results={args.max_results}.")
                    return 0

    if not count:
        print("No direct relative call sites found.")
        return 2
    print(f"Found {count} direct call site(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
