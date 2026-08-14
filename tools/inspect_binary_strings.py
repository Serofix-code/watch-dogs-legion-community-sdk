"""Print narrowly filtered printable strings from a local binary.

This is a research aid, not an extraction tool: callers must provide one or
more case-insensitive filters and results are capped. Nothing is written.
"""

from __future__ import annotations

import argparse
import mmap
import re
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("binary", type=Path)
    parser.add_argument("--contains", action="append", required=True, help="Case-insensitive substring; repeatable")
    parser.add_argument("--minimum", type=int, default=5)
    parser.add_argument("--maximum-length", type=int, default=180)
    parser.add_argument("--max-results", type=int, default=200)
    parser.add_argument("--range-start", type=lambda value: int(value, 0), default=0)
    parser.add_argument("--range-length", type=lambda value: int(value, 0), default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.minimum < 4 or args.maximum_length < args.minimum:
        raise SystemExit("Invalid string-length bounds.")
    if args.max_results < 1 or args.max_results > 5000:
        raise SystemExit("--max-results must be between 1 and 5000.")
    filters = [value.encode("ascii", "strict").lower() for value in args.contains]
    pattern = re.compile(rb"[\x20-\x7e]{%d,%d}" % (args.minimum, args.maximum_length))
    seen: set[bytes] = set()
    emitted = 0
    with args.binary.open("rb") as stream, mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ) as data:
        start = args.range_start
        end = len(data) if args.range_length is None else min(len(data), start + args.range_length)
        if start < 0 or start >= end:
            raise SystemExit("The requested scan range is outside the binary.")
        for match in pattern.finditer(data, start, end):
            raw = match.group(0)
            lowered = raw.lower()
            if not any(value in lowered for value in filters) or raw in seen:
                continue
            seen.add(raw)
            print(f"0x{match.start():X}\t{raw.decode('ascii')}")
            emitted += 1
            if emitted >= args.max_results:
                break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
