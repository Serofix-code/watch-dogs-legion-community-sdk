# v0.12.0 — Cross-renderer FreePhoto Map

This release adds the exact Steam DX12 module fingerprint for changelist `2073645` and independently maps its built-in FreePhoto camera path.

## Confirmed parity

- `CCameraFreePhotoComponent` remains a `0x410`-byte object with the same transform, input, speed, and accumulator offsets.
- The manager interface remains at outer-object `+0x2E8`; its runtime helper remains at interface `+0x318` and is `0x160` bytes.
- Mode `5`, guarded interface slot `+0x28`, the event-dispatch structure, and cleanup-before-delete ordering match DX11.

## Confirmed renderer differences

DX12 has its own executable RVAs, published manager global, vtables, helper tables, and raw action ID. In particular, the mapped mode-5 action ID is `0x5349BB24` in DX12 and `0x81489DE8` in DX11. Consumers must select constants by exact module fingerprint.

## Safety and remaining work

This is static, read-only compatibility research. No proprietary binaries are included, no game process was started during the DX12 analysis, and no external activation implementation is supplied. Runtime activation, callback-thread identity, orientation signs, interruption behavior, and teardown after transitions still require observation before companion integration is considered safe.
