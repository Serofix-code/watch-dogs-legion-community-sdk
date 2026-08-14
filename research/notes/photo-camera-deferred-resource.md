# Deferred photo-request resource ownership

This note extends the cross-renderer deferred request map with the paired resource-lifecycle calls made by its selected branches. Analysis is static and read-only against the exact Steam modules in `docs/BUILDS.md`.

## Acquire path

The DX11 deferred consumer calls RVA `0x244DB80` from `0x33244F5`; DX12 calls its matching implementation at `0x244DDA0` from `0x3324725`.

Acquire returns immediately if resource byte `+0xF0` is already set. Otherwise it sets that byte, copies source handle `+0x100` to owned handle `+0xF8`, rejects invalid `-1` handle forms, calls virtual slot `+0x370`, and tail-dispatches virtual slot `+0x378` with the owned-handle address and the caller's mode argument.

## Release path

The DX11 deferred consumer calls RVA `0x244DBF0` from `0x3324571`; DX12 calls matching RVA `0x244DE10` from `0x33247A1`.

Release acts only when active byte `+0xF0` is set. It clears the byte, validates owned handle `+0xF8`, optionally invokes virtual slot `+0x380`, and then writes `0xFFFFFFFFFFFFFFFF` to `+0xF8`.

## Interpretation boundary

This proves that the deferred request owns a real engine resource with paired acquire/release semantics; it is not merely a delayed Boolean toggle. The formal resource type and handle meaning remain unresolved. It may represent the photo application, input ownership, a world capability, or another prerequisite. A companion must not fabricate this object or handle. Runtime observation must establish its lifetime relative to helper creation, component creation, mode `5`, interruption, and teardown.
