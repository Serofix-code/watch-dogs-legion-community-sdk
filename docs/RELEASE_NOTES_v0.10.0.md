# v0.10.0 — FreePhoto Input and Pitch Mapping

This release connects the engine-owned runtime helper to its normal input/event subscription and resolves one of the three FreePhoto orientation fields.

## New evidence

- helper event-subscription object size `0x10` and type table RVA `0xA116F90`;
- owner back-pointer at subscription `+0x08`;
- event-dispatch thunk RVA `0x33328C0`, which validates the owner and enters the bounded dispatcher;
- state-callback thunk RVA `0x3333090`;
- build-specific FreePhoto action identifier `0x81489DE8` at RVA `0xB3BEFB4`, selected by both mode-5 registration and dispatch;
- quaternion-to-Euler routine RVA `0x323AA10` and confirmed pitch at component `+0x74`.

The database contains 47 evidence records after this release.

## Observer update

Component observations now expose `pitch` separately from `axis0Unknown` and `axis2Unknown`. The helper observer from v0.9.1 continues to report selected mode, event subscription, and transition tokens using query/read access only.

## Limitations

The action's symbolic name, callback thread, service-result semantics, the names of axes `+0x70` and `+0x78`, and interruption/teardown behavior still require runtime evidence. No companion activation code is included.
