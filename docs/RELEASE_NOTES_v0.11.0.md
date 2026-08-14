# v0.11.0 — FreePhoto Input Observation

This release maps the live input fields that drive the built-in FreePhoto component and makes them available through the query/read-only observer.

## Mapped fields

- movement input vector at component `+0x21C`;
- pitch input at `+0x234`;
- yaw input at `+0x238`;
- roll input at `+0x23C`;
- pitch/roll/yaw accumulators at `+0x1BC/+0x1C0/+0x1C4`.

The native update path multiplies each rotation input by its reflected speed field before updating the corresponding accumulator. Movement input is multiplied by `fCameraMoveSpeed` before the camera basis is applied.

## Observer update

`observe_photo_camera.py --scan-components --watch --json` now reports movement input, named rotation inputs, named angle accumulators, position, orientation, limits, speeds, and the backend handle for each structurally validated component candidate.

The observer still opens the game with query/read access only. It does not allocate, inject, hook, suspend, change memory protection, or write.

## Remaining work

Runtime observation is still required for positive/negative direction conventions, callback-thread identity, activation results, and interrupted teardown. No companion activation code is included.
