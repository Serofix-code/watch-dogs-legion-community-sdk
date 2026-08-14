# v0.14.0 — Deferred Photo Request Lifecycle

This release maps a higher-level, cross-renderer photo-camera request path that queues work for later manager processing.

## Confirmed path

- guarded requester: DX11 `0x308FC70`, DX12 `0x308FEA0`;
- rejection feedback through manager slot `+0x88`;
- accepted request through manager slot `+0x20`;
- queue setter: DX11 `0x329390`, DX12 `0x3295C0`;
- deferred consumer entry: DX11 `0x3324370`, DX12 `0x33245A0`;
- interface request bytes `+0x330/+0x331/+0x333`, corresponding to manager `+0x618/+0x619/+0x61B`.

The consumer checks live world/application services, branches on the request selector, and clears the pending flag after handling.

## Safety conclusion

The native application path separates request submission from processing. Calling manager setup, constructing its helper, or invoking the FreePhoto toggle directly would bypass this deferral and its state checks. The scheduler/thread contract and the transition into FreePhoto mode `5` still require runtime observation, so no companion activation implementation is included.
