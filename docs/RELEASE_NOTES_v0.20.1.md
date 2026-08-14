# v0.20.1 — Deferred-request RVA Correction

This corrective release fixes four truncated RVAs in the deferred photo-request record for the exact Steam DX11 and DX12 builds in `BUILDS.md`.

## Corrections

- DX11 queue setter: `0x3329390`.
- DX12 queue setter: `0x33295C0`.
- DX11 rejection feedback: `0x3329080`.
- DX12 rejection feedback: `0x33292B0`.

Direct disassembly confirms that both corrected queue setters write `0x0101` to interface bytes `+0x330/+0x331` and set pending byte `+0x333` to one. No behavior claim changed, and the companion remains unchanged.

No proprietary binaries, extracted game objects, or copyrighted game assets are included.
