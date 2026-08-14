"""Find bounded x64 indirect calls through a specified vtable displacement."""

from __future__ import annotations

import argparse
from pathlib import Path

import pefile
from capstone import CS_ARCH_X86, CS_MODE_64, Cs
from capstone.x86 import X86_OP_MEM


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("binary", type=Path)
    parser.add_argument("displacement", type=lambda value: int(value, 0))
    parser.add_argument("--max-results", type=int, default=200)
    parser.add_argument("--section", action="append", default=[])
    parser.add_argument("--rva-start", type=lambda value: int(value, 0), default=0)
    parser.add_argument("--rva-end", type=lambda value: int(value, 0))
    return parser.parse_args()


def raw_candidates(code: bytes, wanted: int):
    cursor = 0
    while True:
        opcode = code.find(b"\xFF", cursor)
        if opcode < 0 or opcode + 2 >= len(code):
            return
        cursor = opcode + 1
        modrm = code[opcode + 1]
        mode = modrm >> 6
        operation = (modrm >> 3) & 7
        rm = modrm & 7
        if operation != 2 or mode not in (1, 2):
            continue
        displacement_start = opcode + 2 + (1 if rm == 4 else 0)
        size = 1 if mode == 1 else 4
        if displacement_start + size > len(code):
            continue
        displacement = int.from_bytes(code[displacement_start:displacement_start + size], "little", signed=True)
        if displacement == wanted:
            yield opcode


def main() -> int:
    args = arguments()
    pe = pefile.PE(str(args.binary), fast_load=True)
    decoder = Cs(CS_ARCH_X86, CS_MODE_64)
    decoder.detail = True
    count = 0
    reported: set[int] = set()

    for section in pe.sections:
        if not section.IMAGE_SCN_MEM_EXECUTE:
            continue
        name = section.Name.rstrip(b"\0").decode("ascii", "replace")
        if args.section and name not in args.section:
            continue
        code = section.get_data()
        section_rva = int(section.VirtualAddress)
        lower = max(0, args.rva_start - section_rva)
        upper = len(code) if args.rva_end is None else min(len(code), args.rva_end - section_rva)
        if upper <= lower:
            continue
        code = code[lower:upper]
        va = pe.OPTIONAL_HEADER.ImageBase + section_rva + lower
        for opcode in raw_candidates(code, args.displacement):
            starts = [opcode]
            if opcode and 0x40 <= code[opcode - 1] <= 0x4F:
                starts.insert(0, opcode - 1)
            for start in starts:
                instruction = next(decoder.disasm(code[start:start + 16], va + start), None)
                if instruction is None or instruction.mnemonic != "call":
                    continue
                if not any(operand.type == X86_OP_MEM and operand.mem.disp == args.displacement for operand in instruction.operands):
                    continue
                if instruction.address in reported:
                    continue
                reported.add(instruction.address)
                print(f"0x{instruction.address:X}  {name:<8}  {instruction.mnemonic:<5} {instruction.op_str}")
                count += 1
                if count >= args.max_results:
                    return 0
                break

    if not count:
        print("No matching indirect calls found.")
        return 2
    print(f"Found {count} indirect call(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
