# v0.17.0 — Scheduler Registration and Destruction

This release extends the photo-camera scheduler map with manager registration and destruction ownership in both fingerprinted renderer builds.

## Confirmed lifecycle

- manager construction inserts the outer object into an engine-owned compact registry;
- published interface slot `+0x0` adjusts by `-0x2E8` before outer destruction;
- outer destruction invokes normal manager teardown through interface slot `+0x10`;
- runtime helper `+0x600` is released only after normal teardown;
- base destruction removes the manager from the compact registry;
- the published manager interface global is cleared before completion.

## Safety boundary

The interface, outer manager, runtime helper, registry membership, and teardown are one ownership chain. The formal registry type, phase-list transfer, callback thread, and synchronization with an in-progress dispatcher remain unresolved. No activation implementation is included.
