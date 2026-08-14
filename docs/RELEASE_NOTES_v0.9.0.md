# v0.9.0 — Native FreePhoto Activation Chain

This release maps the first complete engine-owned caller chain above the guarded FreePhoto manager toggle for the fingerprinted Steam DX11 build.

## New evidence

- native event callback RVA `0x33363C0`;
- dispatcher RVA `0x33328D0–0x3333088`, bounded by PE unwind metadata;
- mode-5 branch RVA `0x3332CC0` and unique activation call site RVA `0x3332CFC`;
- activation caller RVA `0x3336240`, which performs native service checks and invokes manager interface slot `+0x28`;
- explicit separation between the proven native chain and the still-unproven `sta_open_photomode` name association.

The database contains 46 evidence records after this release.

## Tooling

The direct relative-call finder now scans executable bytes for `E8 rel32` candidates and validates each candidate as an exact instruction. This recovers valid calls after inline executable data. Its output is deliberately labelled as candidates and must be corroborated from a known function boundary or PE unwind range.

## Safety and limitations

No game binary, extracted object, save, asset, credential, or bulk string output is included. No companion activation code is released in this milestone. Runtime thread requirements, service ownership, component creation, orientation order, and safe interruption/teardown still require observation in a running game.
