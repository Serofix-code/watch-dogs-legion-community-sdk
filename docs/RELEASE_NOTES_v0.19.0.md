# v0.19.0 — Registered Photo-camera Close Command

This release maps the engine-registered close side of the photo-camera lifecycle for the exact Steam DX11 and DX12 builds in `BUILDS.md`.

## New findings

- `RequestClosePhotoCamera` is paired with matching generated command wrappers in both renderers.
- The command requires zero arguments.
- Its wrappers call dedicated emitters that construct an owned `0x18`-byte event.
- The emitters submit through build-specific engine channel globals instead of directly destroying the manager.
- Event vtables and channel globals are recorded in the machine-readable database.

## Integrity boundary

No matching open command was found. The public command-registry invocation API, event thread, acknowledgement, and interruption behavior remain unresolved, so this release does not claim a complete or safe external activation recipe. The companion remains unchanged.

No proprietary binaries, extracted game objects, or copyrighted game assets are included.
