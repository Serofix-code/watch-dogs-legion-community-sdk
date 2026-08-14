# Changelog

## v0.6.0 — Guarded Free-mode Path

- Mapped the guarded free-photo-mode interface method at vtable slot `+0x28`.
- Distinguished the free-mode state at interface `+0x100` / manager `+0x3E8` from the ordinary requested state at `+0x101` / `+0x3E9`.
- Extended the read-only observer to report the free-mode state.
- Added bounded direct-call, vtable-call, encoded-reference, and PE-address inspection improvements for reproducible static research.
- Corroborated the `FreeModeCamera` configuration subsection against pinned public Disrupt-tool schemas without importing proprietary game data.

## v0.5.1 — Read-only Lifecycle Observer

- Added a Windows runtime observer for the published photo-camera manager interface.
- Opens the process with query/read access only and verifies the exact module hash and interface vtable.
- Reports requested state, active state, and helper lifetime without injection or writes.

## v0.5.0 — Native Photo-camera Lifecycle

- Mapped the manager interface's guarded setup and full teardown paths.
- Mapped the Boolean requested-state wrapper and its normal internal toggle.
- Identified requested state, active state, and helper-pointer offsets.
- Documented `CPhotoCameraEventChannel` as downstream mode notification rather than an activation API.
- Kept external activation under development pending game-thread and runtime-lifetime validation.

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
