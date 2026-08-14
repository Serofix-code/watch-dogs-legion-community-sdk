# Photo-camera runtime and free-camera component

This note records static, read-only analysis of the Steam DX11 module whose SHA-256 is `086968CD9EC4D5939248846EAFA2DA72210FDDEB1164E79CBD08164313A0086E`. RVAs are build-specific and are not claimed to work on other versions.

## CCameraFreePhotoComponent

The reflected `CPhotoCameraConfig` registration associates its factory with the native `CCameraFreePhotoComponent` factory at RVA `0x32390F0`. The factory allocates `0x410` bytes and calls the constructor at RVA `0x323A110`; the destructor is at RVA `0x323A370` and the main vtable is at RVA `0xA0FC380`.

The component registers against the `CameraFreePhotoComponent` action/event name and installs scheduled callbacks. The update callback at RVA `0x323DE30` invokes the core transform routine at RVA `0x323CA60`.

Confirmed field consumers in this build include:

| Component offset | Meaning | Evidence |
| --- | --- | --- |
| `+0x70/+0x74/+0x78` | three orientation angles | sine/cosine transform construction and later backend update |
| `+0x188` | maximum distance from player | reflected name and movement/clamp path |
| `+0x18C` | camera move speed | reflected name and movement-vector multiplication |
| `+0x194/+0x198/+0x19C` | camera position XYZ | copied into the internal transform and passed to the backend camera |
| `+0x1C8/+0x1CC` | minimum/maximum pitch | reflected names and `maxss`/`minss` clamp |
| `+0x1F4` | orbit movement speed | reflected name and orbit-input multiplication |
| `+0x280` | backend camera handle | null checks and virtual update calls |
| `+0x290` | internal transform structure | transform builder destination |

The position layout is confirmed as a contiguous three-float vector. The three orientation fields are confirmed as angular inputs, but their semantic axis order is not yet runtime-validated. The movement path multiplies the component input vector by `fCameraMoveSpeed`, applies the camera basis, and later evaluates the configured player-distance limit.

## CPhotoCameraManager

Startup code at RVA `0x321A540` allocates a `0x770`-byte manager and calls constructor RVA `0x3320530`. It publishes the interface subobject at `object + 0x2E8` through a build-specific global at RVA `0xB486020`. That address must not be treated as a stable public pointer until its lifetime is observed at runtime.

The interface vtable at RVA `0xA116C00` contains a paired setup/teardown path:

- slot `+0x08`, RVA `0x3326D60`, validates prerequisites, creates camera/controller resources, installs an action map, and sets the active byte at interface offset `+0x102`;
- slot `+0x10`, RVA `0x3327440`, validates the same prerequisites, removes those resources, and clears `+0x102`.

These semantic names are **strongly inferred**, not runtime-confirmed. Calling either method externally without the correct game thread and gameplay state may be unsafe.

## Higher-level entry clue

The application enum-to-string switch at RVA `0x3073F60` maps numeric value `16` to `PhotoCamera`. This may provide a safer app-level entry route than calling manager internals, but its launch caller and argument contract remain unresolved.

## Implementation status

This work replaces the unsuccessful global float-calibration approach with a concrete native component and transform map. It is sufficient for targeted runtime observation, but not yet sufficient for a public trainer implementation. Required next evidence is:

1. observe manager/interface lifetime in active gameplay;
2. identify the normal app-level activation caller or validate the lifecycle call on the game thread;
3. confirm orientation axis order and position changes while photo mode is active;
4. confirm teardown after interruption and save/load transitions.
