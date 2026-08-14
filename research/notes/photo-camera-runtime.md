# Photo-camera runtime and free-camera component

This note records static, read-only analysis of the Steam DX11 module whose SHA-256 is `086968CD9EC4D5939248846EAFA2DA72210FDDEB1164E79CBD08164313A0086E`. RVAs are build-specific and are not claimed to work on other versions.

## CCameraFreePhotoComponent

The reflected `CPhotoCameraConfig` registration associates its factory with the native `CCameraFreePhotoComponent` factory at RVA `0x32390F0`. The factory allocates `0x410` bytes and calls the constructor at RVA `0x323A110`; the destructor is at RVA `0x323A370` and the main vtable is at RVA `0xA0FC380`.

The component registers against the `CameraFreePhotoComponent` action/event name and installs scheduled callbacks. The update callback at RVA `0x323DE30` invokes the core transform routine at RVA `0x323CA60`.

Manager setup does not directly call the component constructor. It creates a separate `0x160`-byte helper, configures engine services and the mode-specific action map, and dispatches the selected camera mode. The component remains engine-owned and is created through the registered component/factory path. Consequently, calling manager setup alone or fabricating a component would bypass required ownership work.

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

### Engine-owned runtime helper

Setup allocates the object stored at interface `+0x318`; it is a concrete `0x160`-byte runtime helper, not the FreePhoto camera component. Its constructor is at RVA `0x3333170`, its type table is at RVA `0xA116FC0`, and the table's single delete thunk at RVA `0x346C150` is immediately followed by the literal `PhotoCameraManager`. The outer `0x770`-byte object remains separately identified by the `CPhotoCameraManager` literal adjacent to its interface table.

After construction, setup calls RVA `0x3327130` to apply the selected mode and RVA `0x33271E0` to acquire input/context services and install an event subscription. Confirmed helper fields include input service `+0x20`, camera context `+0x28`, selected mode `+0x38`, event subscription `+0xD0`, mode-registration byte `+0x120`, and transition tokens `+0xC8`, `+0x14C`, and `+0x154`. The native FreePhoto event path reads mode `+0x38` and retires/replaces token `+0x154`.

Teardown does not simply free this object. It first calls cleanup RVA `0x33279A0`, which releases camera/event context, resets input state, cancels all three mapped transition tokens, unregisters the event subscription, and clears owned service/context pointers. Only then does teardown null interface `+0x318` and call the helper's delete thunk. This strengthens the requirement to use the outer manager lifecycle instead of directly creating, deleting, or invoking the helper.

The distinct toggle at RVA `0x3326A60` changes manager byte `+0x3E8` (interface byte `+0x100`). It requires manager pointers at `+0x348` and `+0x468`, conditionally checks `+0x478`, propagates the new mode to related systems, and invokes interface setup or teardown rather than directly fabricating a camera object. The static control flow and the dedicated `+0x28` interface slot strongly indicate that this is the native free-photo-mode route. It remains **strongly inferred**, not confirmed, until its state transition and component lifetime are observed in a running game.

The guard behind interface slot `+0x40` resolves to RVA `0x3328190`. It is a broad availability test rather than a pointer-only check: it queries live gameplay services, rejects several incompatible state flags, and verifies additional controller/world conditions before permitting entry. If the guard rejects entry, the wrapper passes `false` to interface slot `+0x88` (RVA `0x3329080`). That method manages a Boolean-selected transition/feedback path; the static evidence does not justify calling it a teardown method or activation method.

The native mode identity is now independently corroborated inside the runtime path. When the ordinary requested-state toggle enters, it publishes mode value `5`; the free-mode toggle also publishes mode value `5`. During setup, the selected-mode byte is compared with `5` and mapped to action-map mask `0x100000`. The same setup switch maps mode `0` to `0x20` and mode `6` to `0x04000000`. This agrees exactly with the archive-backed `FreePhoto = 5` record and confirms that mode `5` is not merely a menu label.

Two ordinary consumers at RVAs `0x3332BD9` and `0x3336C18` load the published manager interface global, preserve the `+0x2E8` subobject adjustment, and invoke vtable slot `+0x98` with a Boolean value. The slot resolves to RVA `0x33299F0`; it is mode-aware and treats current mode `5` specially, but it is a downstream notification/state handler rather than the guarded free-mode entry slot. This establishes a real post-startup consumer of the published interface while keeping activation and notification separate.

### Native event activation chain

PE unwind metadata bounds a native event dispatcher at RVA `0x33328D0` through `0x3333088`. A single direct caller at RVA `0x33365CE`, inside callback RVA `0x33363C0`, copies the incoming engine event to a local buffer before entering that dispatcher.

The dispatcher branch beginning at RVA `0x3332CC0` first matches a build-specific action identifier and requires manager/controller byte `+0x38` to equal mode `5`. It asks RVA `0x332A080` to construct or publish value `4`, stores the returned token at controller offset `+0x154`, checks a native prerequisite, and calls RVA `0x3336240` from RVA `0x3332CFC`.

RVA `0x3336240` is the first mapped engine-owned activation caller above the guarded manager wrapper. It resolves live services, retires any token held at controller `+0x154`, asks RVA `0x332A080` to publish value `5`, performs two further service checks, loads the published manager interface at RVA `0xB486020`, and invokes vtable slot `+0x28`. This connects an ordinary event path to the previously mapped FreePhoto toggle without bypassing its availability guard.

This chain is **not yet a supported external call recipe**. The symbolic action name, callback thread, service contracts, ownership of the controller object, and interruption/teardown behavior remain unresolved. The separate `sta_open_photomode` string accessor has not been proven to name this action, so that association is intentionally not claimed.

Manager code also publishes mode-change objects through `CPhotoCameraEventChannel`. This is downstream state notification, not sufficient evidence that publishing an event activates the camera.

## Independent schema corroboration

The zlib-licensed [Gibbed Disrupt tools](https://github.com/gibbed/Gibbed.Disrupt/tree/8c41fe50fabf2eb5673919ef6b5fff1c09186381) document WDL's FAT5 archive format and name hashing in source. A separate WDL definition set pins `FreeModeCamera` inside `PhotoCameraConfig` with enter, exit, movement-start, and movement-end fields ([schema at commit `1d3c3b4`](https://github.com/qstlijku/Gibbed-Tools/blob/1d3c3b447d977d2220b0a6948805766b31e84bcf/projects/WDL/binary%20objects/classes/Photocameraconfig_40469731.binaryclass.xml)). This corroborates the subsection classification but does not by itself prove the runtime activation contract.

## Higher-level entry clue

The application enum-to-string switch at RVA `0x3073F60` maps numeric value `16` to `PhotoCamera`. This may provide a safer app-level entry route than calling manager internals, but its launch caller and argument contract remain unresolved.

## Implementation status

This work replaces the unsuccessful global float-calibration approach with a concrete native component and transform map. The read-only observer can optionally locate exact-vtable component candidates and refresh their mapped transform fields. It is sufficient for targeted runtime observation, but not yet sufficient for a public trainer implementation. Required next evidence is:

1. observe the published manager/interface pointer and state bytes in active gameplay;
2. observe event callback RVA `0x33363C0`, activation caller RVA `0x3336240`, vtable slot `+0x28`, interface byte `+0x100`, and the component lifetime during an ordinary in-game photo-mode transition;
3. confirm orientation axis order and position changes while photo mode is active;
4. confirm teardown after interruption and save/load transitions.
