"""Find direct x64 E8-relative call candidates targeting an address in a PE."""

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
        section_data = section.get_data()
        relative_start = start_rva - section_rva
        relative_end = min(end_rva - section_rva, len(section_data))
        data = section_data[relative_start:relative_end]
        position = data.find(b"\xE8")
        while position >= 0:
            if position + 5 <= len(data):
                instruction_va = image_base + start_rva + position
                displacement = int.from_bytes(data[position + 1:position + 5], "little", signed=True)
                destination = instruction_va + 5 + displacement
                if destination == target:
                    decoded = next(decoder.disasm(data[position:position + 5], instruction_va), None)
                    if decoded is not None and decoded.mnemonic == "call" and len(decoded.operands) == 1:
                        operand = decoded.operands[0]
                        if operand.type == CS_OP_IMM and operand.imm == target:
                            raw = decoded.bytes.hex(" ")
                            rva = decoded.address - image_base
                            print(f"RVA=0x{rva:X} VA=0x{decoded.address:X} bytes={raw}")
                            count += 1
                            if count >= args.max_results:
                                print(f"Stopped at --max-results={args.max_results}.")
                                return 0
            position = data.find(b"\xE8", position + 1)

    if not count:
        print("No direct E8-relative call candidates found.")
        return 2
    print(f"Found {count} direct E8-relative call candidate(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
