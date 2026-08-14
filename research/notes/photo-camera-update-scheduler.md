# Photo-camera manager update scheduler

This note records a read-only, cross-renderer trace from the deferred photo request into its engine-owned update scheduling. RVAs apply only to the exact Steam module fingerprints in `docs/BUILDS.md`.

## Manager update

DX11 RVA `0x331FA70` and DX12 RVA `0x331FCA0` are matching manager-update functions. The embedded symbol family identifies the containing operation as `CPhotoCameraManager::xxxUpdate`. Each function receives the outer manager pointer and directly calls the deferred consumer:

- DX11 call site `0x331FB9F` to `0x3324370`;
- DX12 call site `0x331FDCF` to `0x33245A0`.

After the deferred consumer returns, the same update reads selector byte `+0x618` and pending byte `+0x61B`, performs additional service/state work, can requeue by writing `+0x61B`, and finishes with another manager-relative update. This ordering is further evidence that the consumer is one phase of a larger engine-controlled lifecycle.

## List dispatchers

The manager update has two direct callers in each renderer:

- DX11 `0x348F2B0` and `0x348F330`;
- DX12 `0x348F4E0` and `0x348F560`.

Both are matching list dispatchers. Each sets byte `+0x8` while dispatch is active, decodes a compact list descriptor, walks an array of manager pointers, invokes the manager update for every entry, and clears `+0x8` after the loop. One dispatcher uses descriptor/storage fields `+0x18/+0x20`; the other uses `+0x28/+0x30`.

## Interpretation boundary

This resolves the earlier uncertainty about whether the deferred consumer was called by an engine scheduler: it is reached synchronously inside the manager's ordinary update, which is itself invoked from paired engine-owned update lists. The formal scheduler type, names of the two phases, callback thread, and manager registration/removal operations remain unresolved. These dispatchers are not claimed as safe external entry points.
