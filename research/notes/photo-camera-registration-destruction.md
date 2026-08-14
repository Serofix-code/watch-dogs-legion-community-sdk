# Photo-camera scheduler registration and destruction

This note records the cross-renderer construction, registry, and destruction path for `CPhotoCameraManager`. Analysis is static and read-only against the exact Steam module fingerprints in `docs/BUILDS.md`.

## Registry insertion

The DX11 manager constructor at RVA `0x3320530` begins by calling base constructor `0x64FCD30`. DX12 constructor `0x3320760` calls its matching base constructor at `0x64FE130`.

Each base constructor initializes the manager's inherited state and inserts the outer manager pointer into a compact engine-owned registry if it is not already present. The registry pointer globals are DX11 `0xB478AB8` and DX12 `0xB50DAF8`; the compact descriptor and storage fields are registry-relative `+0x60/+0x68`.

This is registration infrastructure, not a public activation function. The exact mechanism that transfers or exposes registered objects to the paired update-phase lists remains unresolved.

## Interface-owned destruction

Shutdown loads the published interface global and calls interface slot `+0x0` with deletion enabled. The slot is an adjustment thunk:

- DX11 thunk `0x346B480` subtracts interface offset `0x2E8` and calls outer destructor `0x3321BE0`;
- DX12 thunk `0x346B6B0` subtracts `0x2E8` and calls outer destructor `0x3321E10`.

The outer destructor preserves engine ownership order. It first invokes normal interface teardown through slot `+0x10` with Boolean `true` (DX11 call site `0x3321E2B`, DX12 `0x332205B`). Later it releases the runtime helper at outer-manager `+0x600` (DX11 site `0x3322137`, DX12 `0x3322367`). It then calls the base registry destructor (DX11 `0x64FCFF0`, DX12 `0x64FE3F0`), which removes the outer manager from the same compact registry.

Finally, the destructor clears the published manager interface global at DX11 `0x332221F` and DX12 `0x332244F` before completing inherited destruction.

## Safety consequence

The published interface, outer manager, runtime helper, scheduler registration, and ordinary teardown form one ownership chain. External code must not cache the published interface across shutdown, allocate a substitute helper, skip interface teardown, or call update-list dispatchers after registry removal. Static evidence still does not establish thread identity or prove how an in-progress dispatch is synchronized with destruction.
