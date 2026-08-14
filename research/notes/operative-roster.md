# Operative roster evidence

Observed on the Steam PC DX11 module `DuniaDemo_clang_64_dx11.dll` on 2026-08-14; exact module SHA-256 remains unknown.

A unique guarded signature identified the manager-capture instruction. The runtime verified the expected original bytes before installing a reversible capture hook. The captured manager exposed a bounded roster count at `+0xE0`, an operative pointer array at `+0x108`, and operative IDs at `+0x1A0`. Census-backed localization IDs resolved to the visible first names and surnames in the observed roster.

These observations are confirmed only for the named session/build evidence. Object type names, complete ownership rules, and cross-build compatibility remain unknown.
