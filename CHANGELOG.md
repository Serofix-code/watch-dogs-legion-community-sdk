# Changelog

## v0.4.1 — Cross-reference Tool Fix

- Suppressed duplicate x64 references caused by decoding one byte into a REX-prefixed instruction.
- Removed an unused cross-reference command-line option.

## v0.4.0 — Photo-camera Runtime Mapping

- Corrected `FreeModeCamera` from an inferred enum value to a reflected configuration subsection.
- Mapped `CPhotoCameraConfig` construction, factory, size, vtable, and component registration.
- Mapped `CCameraFreePhotoComponent`, including position, orientation, movement-speed, pitch-limit, backend-handle, and update fields.
- Mapped the `CPhotoCameraManager` allocation/publication path and strongly inferred paired setup/teardown methods.
- Confirmed phone/application enum value `16` maps to `PhotoCamera`.
- Added bounded disassembly and RIP-relative cross-reference research tools.
- Kept trainer integration under development pending runtime lifecycle validation.

## v0.3.0 — DLL Registration Research

- Added the first exact module fingerprint and embedded build identity.
- Added a bounded, read-only binary-string inspection tool.
- Documented a contiguous Domino mission-scripting symbol cluster.
- Added unresolved recruitment, operative-availability, recruitment-intel, and schedule-override symbols.
- Documented `PhotoCameraConfig` and its explicit `FreeModeCamera` mode.
- Expanded the evidence database from 22 to 38 records without uploading proprietary files or bulk strings.

## v0.2.0 — Runtime and Operative Systems Research

- Expanded the evidence database from 4 to 22 records.
- Documented the game-thread Lua bridge and six observed Lua-facing interfaces.
- Documented player-position, waypoint, and coordinate-capture layouts.
- Added operative biography, statistics, appearance, perk-container, and contract-schedule research.
- Classified clothing reward handoff as an incomplete result rather than a successful unlock.
- Added three focused evidence notes and regenerated the searchable research index.

## v0.1.0 — Initial Research Release

- MIT-licensed public community SDK repository.
- Evidence-bearing research schema and initial records.
- Searchable Python SDK reader and command-line query tool.
- Database, duplicate-symbol, and broken-reference validation.
- Deterministic generated research index.
- Initial operative, census, signature, and camera research notes.
- GitHub Actions and community issue/PR templates.

The initial release is intentionally incomplete. Unknowns remain first-class database values.
