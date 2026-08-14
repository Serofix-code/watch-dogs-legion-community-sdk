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

The interface vtable at RVA `0xA116C00` contains a paired setup/teardown path, a guarded free-mode toggle, and a normal camera-state request wrapper:

- slot `+0x08`, RVA `0x3326D60`, validates manager fields `+0x60` and `+0x180`, creates a `0x160`-byte helper at interface offset `+0x318`, installs camera/controller resources and an action map, then sets active byte `+0x102`;
- slot `+0x10`, RVA `0x3327440`, requires those same prerequisites and active state, releases the helper and registered resources, then clears `+0x102`;
- slot `+0x28`, RVA `0x33293B0`, is a no-argument guarded toggle. It permits shutdown when interface byte `+0x100` is already set; otherwise it consults virtual guard slot `+0x40`. The allowed branch adjusts from the interface subobject to the manager base and tail-calls RVA `0x3326A60`;
- slot `+0x30`, RVA `0x3329400`, accepts a Boolean requested state, compares it with byte `+0x101`, adjusts from the interface subobject to the manager base, and tail-calls the internal toggle at RVA `0x3326870` only when a change is needed.

The internal toggle changes manager byte `+0x3E9` (the same storage as interface byte `+0x101`), updates related gameplay/UI state, and calls the virtual setup or teardown method. This establishes slot `+0x30` as the closest mapped route to the engine's own requested-state lifecycle. It is preferable to calling setup directly, but its public acquisition and thread contract are still not runtime-confirmed.

The distinct toggle at RVA `0x3326A60` changes manager byte `+0x3E8` (interface byte `+0x100`). It requires manager pointers at `+0x348` and `+0x468`, conditionally checks `+0x478`, propagates the new mode to related systems, and invokes interface setup or teardown rather than directly fabricating a camera object. The static control flow and the dedicated `+0x28` interface slot strongly indicate that this is the native free-photo-mode route. It remains **strongly inferred**, not confirmed, until its state transition and component lifetime are observed in a running game.

Manager code also publishes mode-change objects through `CPhotoCameraEventChannel`. This is downstream state notification, not sufficient evidence that publishing an event activates the camera.

## Independent schema corroboration

The zlib-licensed [Gibbed Disrupt tools](https://github.com/gibbed/Gibbed.Disrupt/tree/8c41fe50fabf2eb5673919ef6b5fff1c09186381) document WDL's FAT5 archive format and name hashing in source. A separate WDL definition set pins `FreeModeCamera` inside `PhotoCameraConfig` with enter, exit, movement-start, and movement-end fields ([schema at commit `1d3c3b4`](https://github.com/qstlijku/Gibbed-Tools/blob/1d3c3b447d977d2220b0a6948805766b31e84bcf/projects/WDL/binary%20objects/classes/Photocameraconfig_40469731.binaryclass.xml)). This corroborates the subsection classification but does not by itself prove the runtime activation contract.

## Higher-level entry clue

The application enum-to-string switch at RVA `0x3073F60` maps numeric value `16` to `PhotoCamera`. This may provide a safer app-level entry route than calling manager internals, but its launch caller and argument contract remain unresolved.

## Implementation status

This work replaces the unsuccessful global float-calibration approach with a concrete native component and transform map. It is sufficient for targeted runtime observation, but not yet sufficient for a public trainer implementation. Required next evidence is:

1. observe the published manager/interface pointer and state bytes in active gameplay;
2. observe vtable slot `+0x28`, interface byte `+0x100`, and the component lifetime during an ordinary in-game photo-mode transition;
3. confirm orientation axis order and position changes while photo mode is active;
4. confirm teardown after interruption and save/load transitions.
