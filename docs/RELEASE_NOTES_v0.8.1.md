# v0.8.1 — Read-only Component Locator

This patch release adds a bounded observation path for the engine-owned free-photo camera component.

## Tooling

- `observe_photo_camera.py --scan-components` scans readable private memory once for the exact supported-build component vtable.
- Candidate objects must remain readable, retain the exact vtable, and contain finite mapped transform/configuration fields.
- `--watch` refreshes position, orientation, pitch limits, movement speeds, and backend-handle values for surviving candidates.
- `--max-scan-mib` and `--max-components` bound the operation.

The observer still requests query/read access only. It never allocates, injects, hooks, suspends threads, changes protection, or writes.

## Research status

Static tracing shows that manager setup dispatches through engine services rather than directly allocating `CCameraFreePhotoComponent`. Candidate correlation during an ordinary in-game transition is still required; this release does not claim external activation is safe.
