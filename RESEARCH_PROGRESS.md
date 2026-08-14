# Research progress

Last updated: 2026-08-14.

## Confirmed for the observed Steam PC DX11 session

- Guarded operative-manager capture signature behavior.
- Operative roster count, pointer array, and operative ID traversal.
- Census-backed first-name and surname localization resolution.
- Engine-thread Lua command handoff and visible entity spawning/removal.
- Reticle-hit coordinates and active-player/world coordinate capture.
- Map-waypoint coordinate capture.
- Biography event, age, income, and NPC status layouts with immediate readback.
- Exact Steam DX11 module fingerprint, embedded changelist, milestone, and build date.
- `CPhotoCameraConfig` construction, destruction, factory, object size, and registration with `CCameraFreePhotoComponent`.
- `CCameraFreePhotoComponent` object size, position vector, orientation block, speed/limit fields, backend handle, and update routine.
- Phone/application enum value `16` maps to `PhotoCamera` in the observed build.
- The fingerprinted archive config maps photo-camera modes Normal `0`, Selfie `1`, FreePhoto `5`, and PhotoBooth `6`; FreePhoto FOV is configured from `45` to `90`.
- The native free-mode and requested-state paths publish mode `5`, and setup maps mode `5` to the dedicated `0x100000` action-map mask.

## Strongly inferred / inferred

- The packed 24-byte operative appearance record uses version 12/type 2 and big-endian bitfields; complete visual persistence is not verified.
- The perk container is a small-vector-style array with two inline 32-bit IDs; safe external allocation is unresolved.
- Contract and attendance traversal resolves participants and time ranges, but ownership and AI scheduling consequences remain unknown.
- `ExecuteReward_V2` accepts readable ItemDB names, but queue consumption does not prove reward ownership.
- `TriggerRuleSmithRule` accepts candidate numeric rules, but independent progression readback is still required.
- A contiguous Domino mission-operation cluster strongly indicates registration metadata for recruitment, operative, objective, persistence, and world operations; signatures and parameter descriptors remain unresolved.
- `FreeModeCamera` is a reflected `PhotoCameraConfig` subsection, not an enum value.
- `CPhotoCameraManager` startup publication, guarded setup/teardown, requested-state wrapper, and distinct free-mode toggle wrapper are mapped. Interface slot `+0x28` routes through a broad availability guard and a `+0x3E8` state transition; runtime and thread requirements still need confirmation.
- A native event callback, bounded dispatcher, mode-5 branch, and engine-owned activation caller are mapped through the guarded `+0x28` FreePhoto toggle. The symbolic action identity and safe external invocation contract remain unresolved.
- The engine-owned `0x160`-byte runtime helper is mapped from construction through input/event subscription and transition-token cleanup; the read-only observer can validate these fields during a future live session.

## Unknown / unresolved

- Runtime result of the native activation chain and guarded free-mode wrapper, game-thread contract, orientation axis order, and interruption/reset behavior.
- Names and semantics for photo-camera mode values `2`, `3`, and `4`.
- Recruitment insertion and ownership semantics.
- Raw save codec, integrity rules, and safe cross-save operative transfer.
- Complete Lua binding, event dispatch, UI factory, command, type, and reflection registries.
- Per-build signature matrix and DX12/non-Steam fingerprints.
- Complete entity ownership and lifetime rules for Lua-spawned objects.
- Reward result/persistence acknowledgement separate from game-thread handoff.

## Camera result

The first fully automatic scan reached one scalar after 85 exported stages, but the survivor oscillated only from approximately `367.0000` to `367.0078` across both axes and is classified as a false positive. Static tracing has now superseded that approach: the native free-photo-camera position is the three-float vector at component offset `+0x194`, with orientation angles at `+0x70`. Runtime activation and teardown validation remain outstanding.

Guiding question: **What systems have we not mapped yet?**
