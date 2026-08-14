# v0.20.0 — Photo-camera Close-event Ownership

This release maps the ownership and native producer topology of the `RequestClosePhotoCamera` event for the exact Steam DX11 and DX12 builds in `BUILDS.md`.

## New findings

- The same `0x18`-byte close-event type is emitted by the registered command and two additional native producers in each renderer.
- Matching clone routines copy the event's shared fields and retain the referenced shared object.
- Event vtables, manager-region producers, UI/state producers, clone routines, and channel globals are recorded for both renderers.
- The UI/state producer's conditional emission state machine is documented without assigning an unsupported class name.

## Integrity boundary

The consumer callback, dispatch thread, acknowledgement, interruption behavior, and matching open request remain unresolved. This release therefore documents a stronger engine-owned teardown contract but does not claim a complete or safe external activation recipe. The companion remains unchanged.

No proprietary binaries, extracted game objects, or copyrighted game assets are included.
