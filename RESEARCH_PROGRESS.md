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

## Strongly inferred / inferred

- The packed 24-byte operative appearance record uses version 12/type 2 and big-endian bitfields; complete visual persistence is not verified.
- The perk container is a small-vector-style array with two inline 32-bit IDs; safe external allocation is unresolved.
- Contract and attendance traversal resolves participants and time ranges, but ownership and AI scheduling consequences remain unknown.
- `ExecuteReward_V2` accepts readable ItemDB names, but queue consumption does not prove reward ownership.
- `TriggerRuleSmithRule` accepts candidate numeric rules, but independent progression readback is still required.
- A contiguous Domino mission-operation cluster strongly indicates registration metadata for recruitment, operative, objective, persistence, and world operations; signatures and parameter descriptors remain unresolved.
- `PhotoCameraConfig` contains an explicit `FreeModeCamera` mode with movement actions, but its controller, numeric mode value, and activation path remain unknown.

## Unknown / unresolved

- True freecam transform, owner, writer call site, thread contract, and reset behavior.
- Recruitment insertion and ownership semantics.
- Raw save codec, integrity rules, and safe cross-save operative transfer.
- Complete Lua binding, event dispatch, UI factory, command, type, and reflection registries.
- Per-build signature matrix and DX12/non-Steam fingerprints.
- Complete entity ownership and lifetime rules for Lua-spawned objects.
- Reward result/persistence acknowledgement separate from game-thread handoff.

## Camera result

The first fully automatic run reached one scalar after 85 exported stages, but the survivor oscillated only from approximately `367.0000` to `367.0078` across both camera axes. This is classified as a false-positive continuously changing value, not a validated camera field. Future scanning must preserve separate horizontal and vertical sets, enforce direction reversal, and rank adjacent transform clusters.

Guiding question: **What systems have we not mapped yet?**
