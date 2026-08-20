# Runtime trainer aim/ESP surface

This note records a source-backed, build-scoped research lead found in the local
v7.27.1 companion source. It is not a claim that the calls are a stable public
game API. The helper probes these Lua globals before attempting any action:

- `CAIAgentManager_GetInstance`
- `GetEntitiesInList`
- `GetLocalPlayerEntityId`
- `GetEntityPosition`
- `GetEntityName`
- `GetEntityAngle`
- `SetEntityAngle`
- `StartEntityHighlight`
- `StopEntityHighlight`
- `StopEntityNetHackHighlight`

The source groups them into two experimental paths. The radar path enumerates
the Human group in bounded batches, resolves position/name/angle, and sorts by
angular offset and distance. The highlight path requests a bounded set of
nearby entities and calls the highlight start/stop functions. The aim path
selects the smallest angular-offset candidate and requests a yaw update.

Confidence: **INFERRED** from the v7.27.1 helper source and API-availability
probe. No standalone runtime success is claimed here; the helper must report
the symbol as callable on the exact DX11 build before use. Thread affinity,
entity-handle type, highlight lifetime, and the exact `SetEntityAngle` axis
remain unresolved.
