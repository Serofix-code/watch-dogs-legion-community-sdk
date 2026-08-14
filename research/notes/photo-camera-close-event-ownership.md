# Photo-camera close-event ownership

This note records static, read-only analysis of the event emitted by the registered `RequestClosePhotoCamera` command in the exact Steam DX11 and DX12 modules listed in `docs/BUILDS.md`.

## Cross-producer identity

The same event vtable is referenced from four routines in each renderer:

| Role | DX11 RVA | DX12 RVA |
| --- | ---: | ---: |
| Manager-region producer | `0x33214F0` | `0x3321720` |
| Registered-command emitter | `0x4245C40` | `0x4245E90` |
| Conditional UI/state producer | `0x4FDE970` | `0x4FDEBC0` |
| Clone routine | `0x34753A0` | `0x34755D0` |

The event vtables are DX11 `0xA124760` and DX12 `0xA1B37A0`. All three producers allocate and construct a `0x18`-byte object, install that build's vtable, resolve the same build-specific channel, and submit it through the engine's owned dispatch path. The channel globals are DX11 `0xB298D30` and DX12 `0xB32DD30`.

The manager-region producer has no direct relative-call references in the observed DX11 executable image. It may be reached through a callback, virtual call, or another dynamic registration; its formal owner remains unresolved.

## Copy and retention behavior

The matching clone routines allocate another `0x18`-byte object, copy the base/shared fields at `+0x08` and `+0x10`, increment the shared reference count associated with the copied `+0x10` pointer when non-null, install the same event vtable, and return the clone.

This establishes that the request participates in the engine channel's owned copy/delivery lifecycle. A raw stack object or direct manager teardown would not reproduce that contract safely.

## Conditional UI/state producer

The DX11 routine at `0x4FDE970` and DX12 routine at `0x4FDEBC0` have the same state machine:

1. return early when byte `+0x5C` is already set;
2. adjust to an owning object by `-0xD8`;
3. set bytes `+0x5C` and `+0x70`;
4. emit the close event only when byte `+0x5D` equals one and byte `+0x3A` is nonzero;
5. invoke a follow-up routine at DX11 `0x4FDDEF0` or DX12 `0x4FDE140`.

The field behavior is confirmed, but there is not enough type evidence to assign a formal class name or a more specific UI role.

## Safety boundary

The evidence confirms object ownership and multiple native producers, but not the consumer callback, dispatch thread, acknowledgement, or interruption behavior. It also does not reveal a matching open event or command. Consequently, this record improves the safe teardown model but is not a complete external FreePhoto activation recipe.
