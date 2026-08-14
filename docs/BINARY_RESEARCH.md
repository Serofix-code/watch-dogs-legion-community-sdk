# Responsible local binary research

The repository may document independently derived names, hashes, layouts, and small contextual facts needed for interoperability. It must not contain Ubisoft binaries, assets, saves, decryption keys, bulk string dumps, or reconstructed proprietary source.

## Bounded string inspection

`tools/inspect_binary_strings.py` memory-maps a binary read-only and prints only printable ASCII strings that match an explicit case-insensitive filter. Output is capped and nothing is written.

```bash
python tools/inspect_binary_strings.py path/to/module.dll \
  --contains PhotoCamera \
  --contains FreeModeCamera \
  --max-results 100
```

Optional `--range-start` and `--range-length` values accept decimal or `0x` notation and allow a known PE region to be inspected without scanning the entire file.

## Bounded PE cross-reference and disassembly tools

The repository also includes `find_string_xrefs.py`, `find_rip_xrefs.py`, `show_binary_range.py`, and `disassemble_range.py`. These are local, read-only helpers; they do not copy the inspected binary or create bulk dumps. The PE-aware tools require `pefile` and `capstone`; the optimized RIP-relative scanner additionally requires `numpy`.

```bash
python -m pip install pefile capstone numpy
python tools/find_string_xrefs.py path/to/module.dll PhotoCameraConfig
python tools/find_rip_xrefs.py path/to/module.dll rva:0x9E9ECE8 --max-results 20
python tools/disassemble_range.py path/to/module.dll 0x18323CA60 0x280
```

Keep published output tightly bounded to the evidence necessary for an independently written interoperability record.

## Evidence rules

- Record the exact module digest and build identity.
- Publish only the minimum names and context required to explain the discovery.
- Separate a string's literal presence from any inference about behavior.
- Do not claim a callable function until a registration descriptor or call target is mapped.
- Do not claim gameplay success from queue handoff alone.
- Preserve failed hypotheses and unknown parameters.
