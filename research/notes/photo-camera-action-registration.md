# Photo-camera action registration lifecycle

This note records static, read-only analysis of the mode-dependent action registration used by the photo-camera runtime helper. RVAs apply only to the exact Steam module fingerprints in `docs/BUILDS.md`.

## Engine-owned registration

The matching registration routines are DX11 RVA `0x33337A0` and DX12 RVA `0x33339D0`. Direct relative-call analysis finds exactly two callers in each renderer:

- manager/helper setup calls the routine at DX11 `0x33273CE` and DX12 `0x33275FE`;
- the helper update calls it at DX11 `0x3323FD2` and DX12 `0x3324202` when helper byte `+0xF0` is set, then clears that byte immediately after the call.

The setup path first creates the helper's event-subscription object at `+0xD0` when required, registers that object with the input/event service, and only then invokes the action-registration routine. Registration is therefore part of an established helper lifecycle, not a standalone activation call.

## Mode-dependent action identities

The registration routine reads the helper's selected-mode byte at `+0x38` and chooses a raw 32-bit action identity:

- mode `5` loads the renderer-specific FreePhoto action storage: DX11 RVA `0xB3BEFB4`, observed value `0x81489DE8`; DX12 RVA `0xB453FB4`, observed value `0x5349BB24`;
- mode `6` uses immediate value `0xF6A2885B` in both renderers;
- the remaining branch uses immediate value `0x28033097` in both renderers.

These are opaque runtime identities. No symbolic input names have been established, and the differing mode-5 values prove that callers must not assume the DX11 value is portable to DX12.

## Dirty re-registration

The helper has callbacks that set byte `+0xF0`, after which the ordinary update path performs the registration and clears the byte. Those callbacks are not reached through ordinary direct calls and were not resolved to a public vtable or reflected command. Their formal event names and producer remain unknown.

## Safety boundary

The observed ordering requires a live helper, input/event service, event subscription, and ordinary helper update. Calling the registration routine directly cannot safely create FreePhoto mode and may bypass ownership and cleanup. This result narrows the native path but does not yet justify companion activation or memory writes.
