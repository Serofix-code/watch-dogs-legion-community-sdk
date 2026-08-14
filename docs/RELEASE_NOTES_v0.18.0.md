# v0.18.0 — Photo-camera Action Registration

This research release maps another engine-owned boundary in the built-in photo-camera path for the exact Steam DX11 and DX12 builds documented in `BUILDS.md`.

## New findings

- The mode-dependent registration routines are DX11 RVA `0x33337A0` and DX12 RVA `0x33339D0`.
- Each has exactly two direct callers: helper setup and a helper-update branch guarded by byte `+0xF0`.
- The update branch clears `+0xF0` immediately after registration.
- Mode `5` uses renderer-specific raw identities; mode `6` and the remaining branch use shared immediate identities.
- Setup creates and registers the helper event-subscription object before registering actions.

## Integrity boundary

Raw identities are documented as opaque values. No symbolic action name, public opening command, callback thread, or safe external invocation contract is claimed. The companion remains unchanged because direct registration would bypass required helper ownership and cleanup.

No proprietary binaries, extracted game objects, or copyrighted game assets are included.
