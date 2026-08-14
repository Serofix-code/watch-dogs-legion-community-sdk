# v0.7.0 — Photo-camera Archive Configuration

This release adds bounded, reproducible inspection of named WDL FAT5 entries and confirms the configured photo-camera mode map for the fingerprinted Steam data build.

## Confirmed configuration

- Normal mode: `0`
- Selfie mode: `1`
- FreePhoto mode: `5`
- PhotoBooth mode: `6`
- FreePhoto FOV range: `45` to `90`
- The main config resets its photo-camera mode when reopened.

Values `2`, `3`, and `4` remain unresolved. The release does not invent names for them.

## Tooling

`tools/inspect_fat5_entry.py` resolves one known archive-relative name, reports its FAT5 metadata, and can decode observed uncompressed or scheme-3 content in memory. It prints only hashes and explicitly filtered ASCII strings and has no extraction/output option.

## Integrity and scope

- 45 evidence records
- 5 unit tests
- exact FAT index and decoded-record hashes documented
- no Ubisoft archives, extracted objects, generated XML, assets, saves, or bulk dumps included

This archive evidence corroborates the native free-mode route but does not yet prove that external activation is thread-safe. Companion integration remains pending runtime validation.
