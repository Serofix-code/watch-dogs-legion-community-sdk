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

The repository also includes bounded helpers for strings, RIP-relative references, direct calls, vtable calls, encoded pointers, PE ranges, and disassembly. These are local and read-only; they do not copy the inspected binary or create bulk dumps. The PE-aware tools require `pefile` and `capstone`; the optimized RIP-relative scanner additionally requires `numpy`.

```bash
python -m pip install pefile capstone numpy
python tools/find_string_xrefs.py path/to/module.dll PhotoCameraConfig
python tools/find_rip_xrefs.py path/to/module.dll rva:0x9E9ECE8 --max-results 20
python tools/find_relative_calls.py path/to/module.dll 0x1833293B0 --max-results 20
python tools/find_vtable_calls.py path/to/module.dll 0x28 --rva-start 0x3200000 --rva-end 0x3400000
python tools/find_absolute_pointers.py path/to/module.dll 0x1833293B0 --include-rva32
python tools/show_binary_range.py path/to/module.dll 0x18A116C00 0x40 --pe-address
python tools/disassemble_range.py path/to/module.dll 0x18323CA60 0x280
```

Keep published output tightly bounded to the evidence necessary for an independently written interoperability record.

## Read-only photo-camera runtime observation

`observe_photo_camera.py` opens the game with query/read access only and validates the mapped manager interface against the exact supported module hash and vtable. It reports the distinct free-mode state, ordinary requested state, active state, and helper lifetime without allocating, injecting, hooking, suspending, changing protection, or writing.

```powershell
python tools/observe_photo_camera.py
python tools/observe_photo_camera.py --watch --json
```

The observer refuses unknown module hashes unless `--skip-hash` is explicitly supplied. Unknown builds should be researched and recorded separately rather than assumed compatible.

## Evidence rules

- Record the exact module digest and build identity.
- Publish only the minimum names and context required to explain the discovery.
- Separate a string's literal presence from any inference about behavior.
- Do not claim a callable function until a registration descriptor or call target is mapped.
- Do not claim gameplay success from queue handoff alone.
- Preserve failed hypotheses and unknown parameters.
