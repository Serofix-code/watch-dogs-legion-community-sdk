# Runtime bridges and observed Lua bindings

Observed on Steam PC DX11 on 2026-08-14. The exact module SHA-256 remains unrecorded.

An existing Lua-execution call site can be reached safely only by handing commands to an engine-owned game thread. The independently written research harness used a bounded ten-slot FIFO with 256-byte UTF-8 slots and a monotonically increasing completion counter. The counter proves handoff, not the gameplay result of the command.

Visible clothing-shop entities confirmed `GetReticleHitLocation`, `SpawnEntityFromArchetype`, and `RemoveEntity` as usable in active campaign gameplay. `GetLocalPlayerEntityId` and `GetEntityAngle(..., 2)` supplied player context and orientation. Exact native types and the complete binding registry remain unknown.

`ExecuteReward_V2` is deliberately not classified as confirmed ownership mutation. The game consumed hundreds of readable ItemDB record-name calls without a reliable wardrobe ownership change. This negative result shows why queue completion and operation completion require separate acknowledgements.

`TriggerRuleSmithRule` accepted candidate numeric IDs, but this pass lacks independent balance readback. Its rule registry and persistence contract remain unresolved.

No game binary, extracted asset, raw save, or proprietary implementation is included in this repository.
