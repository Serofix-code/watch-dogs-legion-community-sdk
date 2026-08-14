# v0.16.0 — Photo-camera Update Scheduler

This release corrects the deferred-consumer RVAs and traces the consumer into the engine-owned photo-camera manager update scheduler in both fingerprinted renderer builds.

## Confirmed scheduler path

- manager update: DX11 `0x331FA70`, DX12 `0x331FCA0`;
- deferred consumer: DX11 `0x3324370`, DX12 `0x33245A0`;
- direct consumer call sites: DX11 `0x331FB9F`, DX12 `0x331FDCF`;
- paired list dispatchers: DX11 `0x348F2B0/0x348F330`, DX12 `0x348F4E0/0x348F560`.

The dispatchers enumerate engine-owned manager lists while an in-dispatch flag is set. The manager update synchronously processes the deferred request before continuing with related state work.

## Correction

Four previously published consumer/call-site RVAs were missing one hexadecimal digit. This release corrects the machine-readable records and the v0.14.0/v0.15.0 research notes. Function RVAs for the paired resource acquire/release routines were already correct.

## Remaining boundary

Formal scheduler and phase names, callback thread, manager registration/removal operations, and interrupted teardown remain unresolved. No activation implementation is included.
