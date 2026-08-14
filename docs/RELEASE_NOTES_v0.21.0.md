# v0.21.0 — Smartphone Lua Binding Surface

This release adds a cross-renderer research map for the smartphone Lua binding-name family in the exact Steam DX11 and DX12 builds in `BUILDS.md`.

## New findings

- Ten smartphone operations occur contiguously and in identical order in both renderer binding-name corpora.
- The family covers override activation/clear, app hidden/new/available/installed state, state queries, and app-ID lookup.
- Individual searchable records are included for `SmartphoneActivateOverride`, `SmartphoneClearOverride`, and `SmartphoneGetAppId`.
- The records link to the independently confirmed `PhotoCamera` application enum as a research direction.

## Integrity boundary

String presence does not establish signatures or runtime safety. Registration wrappers, arguments, return values, accepted app identifiers, thread affinity, and cleanup remain unresolved. This release does not claim that these calls open FreePhoto, and the companion remains unchanged.

No proprietary binaries, extracted game objects, or copyrighted game assets are included.
