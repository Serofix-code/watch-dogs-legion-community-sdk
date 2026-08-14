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

`find_relative_calls.py` scans executable bytes for `E8 rel32` candidates and validates each candidate as one exact five-byte Capstone instruction. This avoids losing valid calls when executable sections contain inline data. Results remain candidates because an `E8` byte can occur inside another instruction or embedded data; corroborate important hits from a known function boundary or PE unwind range.

## Focused FAT5 entry inspection

`inspect_fat5_entry.py` resolves one known archive-relative name in a WDL FAT5 version-13 index. It can decode observed uncompressed and scheme-3 entries in memory and print only hashes plus explicitly filtered ASCII strings. It has no extraction/output option.

```bash
python -m pip install lz4
python tools/inspect_fat5_entry.py path/to/common.fat \
  'generated\\databases\\generic\\photocameraconfig_40469731.obj' \
  --decode --contains PhotoCamera --contains FreeMode --max-results 20
```

Do not commit decoded objects, XML conversions, or archive bytes. Record only bounded interoperability facts and hashes.

## Read-only photo-camera runtime observation

`observe_photo_camera.py` opens the game with query/read access only and validates the mapped manager interface against the exact supported module hash and vtable. It reports the distinct free-mode state, ordinary requested state, active state, and helper lifetime without allocating, injecting, hooking, suspending, changing protection, or writing. When the runtime helper exists, the observer also validates its exact type table and reports its selected mode, input/context pointers, event subscription, and three transition tokens.

```powershell
python tools/observe_photo_camera.py
python tools/observe_photo_camera.py --watch --json
python tools/observe_photo_camera.py --scan-components --watch --json
```

`--scan-components` performs one bounded scan of readable private memory for the exact fingerprinted `CCameraFreePhotoComponent` vtable. Matching objects are structurally validated and their mapped position, orientation, limits, movement speeds, and backend-handle fields are refreshed during `--watch`. The scan is opt-in because it can inspect several gigabytes; `--max-scan-mib` and `--max-components` provide explicit bounds.

The observer refuses unknown module hashes unless `--skip-hash` is explicitly supplied. Component matches are candidates until correlated with an ordinary in-game transition. Unknown builds should be researched and recorded separately rather than assumed compatible.

## Evidence rules

- Record the exact module digest and build identity.
- Publish only the minimum names and context required to explain the discovery.
- Separate a string's literal presence from any inference about behavior.
- Do not claim a callable function until a registration descriptor or call target is mapped.
- Do not claim gameplay success from queue handoff alone.
- Preserve failed hypotheses and unknown parameters.
