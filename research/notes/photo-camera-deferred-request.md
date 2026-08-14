# Deferred photo-camera request lifecycle

This note records static, read-only analysis of the exact Steam DX11 and DX12 modules listed in `docs/BUILDS.md`. It identifies a higher-level deferred request path that is distinct from directly invoking manager setup or the guarded FreePhoto toggle.

## Guarded requester

DX11 function RVA `0x308FC70` and DX12 RVA `0x308FEA0` have matching control flow. Each loads the published photo-camera manager interface, calls manager guard slot `+0x48`, performs additional caller- and service-specific checks, and chooses one of two outcomes:

- rejection routes to manager slot `+0x88` with Boolean `true`;
- acceptance performs two additional service calls and tail-calls manager slot `+0x20`.

The exact caller class and symbolic operation name remain unresolved. The structure nevertheless proves that this request passes through broader application/gameplay checks before manager work is queued.

## Queue setter

Manager interface slot `+0x20` resolves to DX11 RVA `0x329390` and DX12 RVA `0x3295C0`. It performs no allocation and does not enter photo mode immediately. Instead, it writes `0x0101` to interface bytes `+0x330/+0x331` and sets interface byte `+0x333` to `1`.

Because the interface subobject begins at outer-manager `+0x2E8`, these fields correspond to manager bytes `+0x618/+0x619/+0x61B`.

## Deferred consumer

The later consumer entry is DX11 RVA `0x3324370` and DX12 RVA `0x33245A0`. It checks manager pending byte `+0x61B`, resolves live world/application services, and rejects processing when the relevant world object or state mask is unavailable. It then branches on manager byte `+0x618`, performs branch-specific service checks and calls, and clears pending byte `+0x61B` before returning from the handled path.

The embedded `CPhotoCameraManager` update symbol family includes `UTDS::xxxUpdateDeferredPhotoRequest`, which strongly explains this routine's role. Cross-renderer direct-call and list-dispatch evidence now establishes its engine-owned update scheduling; see `photo-camera-update-scheduler.md`. The exact callback thread and public scheduling interface remain unknown, so an external game-thread call recipe is not claimed.

## Safety consequence

The engine's higher-level path deliberately separates request submission from processing. Directly calling setup, constructing the helper, or invoking the FreePhoto toggle from an arbitrary external thread bypasses this deferral and the live-state checks. A safe companion implementation still requires runtime observation of the queue transition, helper/component creation, callback thread, and cancellation after interruption or save/load.
