# v0.10.0 — FreePhoto Input and Pitch Mapping

> **Correction:** v0.10.1 supersedes the preliminary orientation label in this release. The verified mapping is pitch `+0x70`, roll `+0x74`, yaw `+0x78`.

This release connects the engine-owned runtime helper to its normal input/event subscription and resolves one of the three FreePhoto orientation fields.

## New evidence

- helper event-subscription object size `0x10` and type table RVA `0xA116F90`;
- owner back-pointer at subscription `+0x08`;
- event-dispatch thunk RVA `0x33328C0`, which validates the owner and enters the bounded dispatcher;
- state-callback thunk RVA `0x3333090`;
- build-specific FreePhoto action identifier `0x81489DE8` at RVA `0xB3BEFB4`, selected by both mode-5 registration and dispatch;
- quaternion-to-Euler routine RVA `0x323AA10`; its orientation labels are corrected by v0.10.1.

The database contains 47 evidence records after this release.

## Observer update

Component observations gained structured Euler-angle output. v0.10.1 corrects the field labels to pitch, roll, and yaw at `+0x70/+0x74/+0x78`.

## Limitations

The action's symbolic name, callback thread, service-result semantics, orientation sign conventions, and interruption/teardown behavior still require runtime evidence. No companion activation code is included.
