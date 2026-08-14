# v0.15.0 — Deferred Resource Ownership

This release extends the deferred photo-camera request map with its paired engine-resource acquire and release lifecycle.

## Confirmed fields and hooks

- active byte `+0xF0`;
- owned handle `+0xF8`;
- source handle `+0x100`;
- prepare/acquire/release virtual slots `+0x370/+0x378/+0x380`;
- DX11 acquire/release RVAs `0x244DB80/0x244DBF0`;
- DX12 acquire/release RVAs `0x244DDA0/0x244DE10`.

Acquire sets active state, copies and validates the handle, and invokes the prepare/acquire hooks. Release clears active state, invokes the release hook when requested, and invalidates the owned handle.

## Remaining boundary

The resource's formal type and meaning are unresolved. It may own the photo application, an input context, a world capability, or another prerequisite. This reinforces that a companion must not fabricate the resource or call the deferred branch internals directly. No activation implementation is included.
