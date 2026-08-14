# v0.8.0 — Native FreePhoto Dispatch

This release connects the archive-backed `FreePhoto = 5` configuration to the fingerprinted module's native runtime control flow.

## New findings

- Both mapped native camera-state paths publish mode value `5` when entering FreePhoto behavior.
- Manager setup maps mode `5` to action-map mask `0x100000`.
- Interface slot `+0x40` resolves to a broad availability guard at RVA `0x3328190`.
- Rejected entry routes to a Boolean transition/feedback method at RVA `0x3329080`; it is not labelled as activation or teardown.
- Ordinary engine consumers reacquire the published interface and invoke a separate mode-aware notification handler at RVA `0x33299F0`.

## Integrity and scope

- 45 evidence records
- no game binaries, archives, extracted objects, assets, saves, or bulk dumps included
- all addresses are build-specific to the documented Steam DX11 module fingerprint

The activation chain is substantially narrower, but external invocation is still under development. Required-thread behavior, live component ownership, orientation order, and interrupted teardown must be runtime-validated before companion integration.
