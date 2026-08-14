# v0.6.0 — Guarded Free-mode Path

This release maps the engine-owned free-photo-mode toggle separately from the ordinary photo-camera requested state for the fingerprinted Steam DX11 build.

## New evidence

- Interface vtable slot `+0x28` resolves to a guarded no-argument wrapper at RVA `0x33293B0`.
- The allowed branch enters a distinct manager toggle at RVA `0x3326A60`.
- Free-mode state is stored at interface `+0x100` / manager `+0x3E8`.
- The distinct toggle coordinates native setup or teardown and related system notifications rather than fabricating a camera object directly.
- Pinned public Disrupt-tool schemas independently corroborate that `FreeModeCamera` is a `PhotoCameraConfig` subsection with enter/exit and movement events.

## Tooling

- The read-only runtime observer now reports free-mode state.
- Added bounded direct-call, vtable-call, absolute/RVA-reference, and PE-address inspection support.

## Status

The static route is **STRONGLY INFERRED**. It is not exposed as a write-capable SDK API and has not been added to the companion. Runtime validation of thread ownership, component creation, transform axes, and teardown is still required.

No Ubisoft binaries, assets, bulk dumps, saves, or proprietary source are included.
