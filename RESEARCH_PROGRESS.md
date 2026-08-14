# Research progress

Last updated: 2026-08-14.

## Confirmed for the observed Steam PC build family

- Guarded operative-manager capture signature behavior.
- Operative roster count, pointer array, and operative ID traversal.
- Census-backed first-name and surname localization resolution.
- Engine-thread Lua command handoff and visible entity spawning/removal.
- Reticle-hit coordinates and active-player/world coordinate capture.
- Map-waypoint coordinate capture.
- Biography event, age, income, and NPC status layouts with immediate readback.
- Exact Steam DX11 module fingerprint, embedded changelist, milestone, and build date.
- Exact Steam DX12 module fingerprint with the same changelist and milestone, plus an independently traced FreePhoto component, manager, activation chain, and ordered helper teardown.
- `CPhotoCameraConfig` construction, destruction, factory, object size, and registration with `CCameraFreePhotoComponent`.
- `CCameraFreePhotoComponent` object size, position vector, orientation block, speed/limit fields, backend handle, and update routine.
- Phone/application enum value `16` maps to `PhotoCamera` in the observed build.
- The fingerprinted archive config maps photo-camera modes Normal `0`, Selfie `1`, FreePhoto `5`, and PhotoBooth `6`; FreePhoto FOV is configured from `45` to `90`.
- The native free-mode and requested-state paths publish mode `5`, and setup maps mode `5` to the dedicated `0x100000` action-map mask.
- The engine-owned `0x160`-byte runtime helper, its event-subscription owner edge, three transition tokens, selected-mode field, and ordered cleanup path.
- The `CPhotoCameraComponent` event bridge to manager slots `+0x98/+0xA0`, including both opaque discriminator values and the helper-state reset at helper `+0x1C`.
- The cross-renderer deferred photo request: a guarded requester queues through manager slot `+0x20`, and a later update validates live services before clearing the pending request.
- The deferred request's paired resource owner, including active/source/owned-handle fields and virtual acquire/release hooks in both renderers.
- The engine-owned manager update and paired list dispatchers that schedule the deferred consumer in both renderers.
- Manager construction/destruction registration, including compact-registry insertion/removal, interface-adjusted deletion, normal teardown before helper release, and published-global clearing.
- Cross-renderer photo-camera action registration, including its setup/update callers, helper dirty flag, selected-mode field, and renderer-specific FreePhoto identities.
- The registered zero-argument `RequestClosePhotoCamera` command and its matching cross-renderer event-emission path.
- The close event's cross-renderer manager, command, and conditional UI/state producers, plus its clone-and-retain ownership contract.
- A cross-renderer ten-name smartphone Lua binding family, including unresolved activate/clear override and app-ID lookup operations.
- FreePhoto component pitch/roll/yaw at `+0x70/+0x74/+0x78`, fixed by reflected speed/limit fields, dedicated accumulators, initialization copies, and quaternion-to-Euler extraction.
- Cross-renderer `CCameraComponent` and separately named `CCameraFreeComponent` static leads, plus the DX11 `CCameraGameProcessingComponent` pre-physics, post-input, post-physics, and post-camera update registrations. `CCameraFreeComponent` additionally exposes reflected pitch/yaw input, follow, pivot, collision, ideal-offset, reticle, lens, blending, and FOV parameter names.

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
- Photo-camera action registration is owned by helper setup and dirty-flagged update; the symbolic action names, dirty-callback producer, and safe public activation contract remain unresolved.
- `RequestClosePhotoCamera` emits a clonable engine-owned close event from three native producer contexts, but its consumer callback, public registry invocation API, callback thread, acknowledgement, and any matching open command remain unresolved.
- The component event bridge is mapped, but its two discriminator names and producer remain unresolved; neither is claimed as an open/close command.
- The deferred request is confirmed inside the engine-owned manager update and paired update-list dispatchers; formal phase names, callback thread, registration/removal operations, and its transition into FreePhoto mode `5` remain unresolved.
- The deferred resource's formal type and whether it owns the app, input, world capability, or another prerequisite remain unresolved.
- The formal scheduler registry type, transfer into the two phase lists, and destruction synchronization with an in-progress dispatcher remain unresolved.
- The smartphone Lua family is present in both renderers, but its registration wrappers, parameters, return types, thread affinity, accepted app identifiers, and override cleanup remain unresolved.

## Unknown / unresolved

- Runtime result of the native activation chain and guarded free-mode wrapper, game-thread contract, orientation sign/direction conventions, and interruption/reset behavior.
- Names and semantics for photo-camera mode values `2`, `3`, and `4`.
- Recruitment insertion and ownership semantics.
- Raw save codec, integrity rules, and safe cross-save operative transfer.
- Complete Lua binding, event dispatch, UI factory, command, type, and reflection registries.
- Per-build signature matrix beyond the mapped Steam DX11/DX12 camera paths, plus non-Steam fingerprints.
- Complete entity ownership and lifetime rules for Lua-spawned objects.
- Reward result/persistence acknowledgement separate from game-thread handoff.

## Camera result

The first fully automatic scan reached one scalar after 85 exported stages, but the survivor oscillated only from approximately `367.0000` to `367.0078` across both axes and is classified as a false positive. Static tracing has now superseded that approach for Photo Mode: the native free-photo-camera position is the three-float vector at component offset `+0x194`, with orientation angles at `+0x70`.

The detached-gameplay target is separate. `CCameraComponent`, `CCameraGameProcessingComponent`, and `CCameraFreeComponent` are now documented as static leads. Their live instances, transform layouts, owner edges, player-follow writer, activation, and cleanup remain unresolved. The companion must remain read-only for this route until those contracts are verified.

Guiding question: **What systems have we not mapped yet?**
