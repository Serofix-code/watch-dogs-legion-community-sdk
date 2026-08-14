# Changelog

## v0.9.1 — Runtime Helper Lifecycle

- Identified and mapped the engine-owned `PhotoCameraManager` runtime helper created by outer manager setup.
- Mapped its mode, input/context, event-subscription, transition-token, and ordered cleanup fields.
- Extended the read-only observer to report the helper lifecycle without writing to the game.

## v0.9.0 — Native FreePhoto Activation Chain

- Mapped the engine event callback and PE-unwind-bounded dispatcher that reach the FreePhoto path.
- Mapped the unique mode-5 activation caller and its guarded manager-interface dispatch.
- Improved direct relative-call discovery across executable sections containing inline data.
- Kept external activation under development pending runtime thread, ownership, and teardown validation.

## v0.8.1 — Read-only Component Locator

- Added an opt-in bounded scan for exact-vtable `CCameraFreePhotoComponent` candidates.
- Added structural validation and live transform-field refresh to the read-only observer.
- Documented that manager setup dispatches through engine ownership instead of allocating the component directly.

## v0.8.0 — Native FreePhoto Dispatch

- Confirmed that native runtime paths publish FreePhoto mode `5`.
- Mapped mode `5` to the dedicated `0x100000` setup action-map mask.
- Mapped the broad free-mode availability guard at RVA `0x3328190`.
- Distinguished rejection feedback and downstream mode notification from activation.
- Documented post-startup consumers of the published manager interface.

## v0.7.0 — Photo-camera Archive Configuration

- Added a no-output, single-entry FAT5 metadata and in-memory inspection tool.
- Documented the fingerprinted photo-camera config/menu records without committing extracted game data.
- Confirmed photo-camera mode values Normal `0`, Selfie `1`, FreePhoto `5`, and PhotoBooth `6`.
- Confirmed the FreePhoto FOV configuration range of `45` to `90`.

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
