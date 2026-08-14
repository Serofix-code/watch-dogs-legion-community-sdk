"""Find x64 RIP-relative code references to an exact ASCII string in a PE file.

The tool is read-only and prints only small instruction windows around exact
references. It depends on the third-party ``pefile`` and ``capstone`` packages.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pefile
from capstone import CS_ARCH_X86, CS_MODE_64, Cs
from capstone.x86 import X86_OP_MEM, X86_REG_RIP


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("binary", type=Path)
    parser.add_argument("text")
    parser.add_argument("--context", type=int, default=4)
    parser.add_argument("--max-results", type=int, default=50)
    return parser.parse_args()


def main() -> int:
    args = arguments()
    pe = pefile.PE(str(args.binary), fast_load=True)
    image_base = pe.OPTIONAL_HEADER.ImageBase
    needle = args.text.encode("ascii") + b"\0"
    raw = args.binary.read_bytes()
    offsets: list[int] = []
    start = 0
    while len(offsets) < args.max_results:
        found = raw.find(needle, start)
        if found < 0:
            break
        offsets.append(found)
        start = found + 1
    targets = {image_base + pe.get_rva_from_offset(offset): offset for offset in offsets}
    if not targets:
        print("String not found.")
        return 1

    decoder = Cs(CS_ARCH_X86, CS_MODE_64)
    decoder.detail = True
    hits: list[tuple[object, int, str]] = []
    for section in pe.sections:
        if not section.IMAGE_SCN_MEM_EXECUTE:
            continue
        code = section.get_data()
        va = image_base + section.VirtualAddress
        instructions = list(decoder.disasm(code, va))
        for index, instruction in enumerate(instructions):
            for operand in instruction.operands:
                if operand.type != X86_OP_MEM or operand.mem.base != X86_REG_RIP:
                    continue
                destination = instruction.address + instruction.size + operand.mem.disp
                if destination in targets:
                    hits.append((instruction, index, section.Name.rstrip(b"\0").decode("ascii", "replace")))
                    lo = max(0, index - args.context)
                    hi = min(len(instructions), index + args.context + 1)
                    print(f"\n{args.text!r} file=0x{targets[destination]:X} VA=0x{destination:X} section={hits[-1][2]}")
                    for current in instructions[lo:hi]:
                        marker = ">" if current.address == instruction.address else " "
                        print(f"{marker} 0x{current.address:X}: {current.mnemonic:<8} {current.op_str}")
                    if len(hits) >= args.max_results:
                        return 0
    if not hits:
        print(f"String exists at {', '.join(f'0x{value:X}' for value in offsets)}, but no direct RIP-relative executable reference was found.")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
