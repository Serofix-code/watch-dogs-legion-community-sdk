# Photo-camera component-to-manager event bridge

This note records static, read-only analysis of the exact Steam DX11 module fingerprinted in `docs/BUILDS.md`. It maps an ordinary `CPhotoCameraComponent` event bridge but does not assign unsupported symbolic names to its events.

## Component identity

The `CPhotoCameraComponent` literal and reflection table are adjacent to two native vtable regions. Constructor RVA `0x32E7A30` installs primary vtable RVA `0xA110EB0` and secondary vtable RVA `0xA110D10`. A function pointer in the same component table resolves to event handler RVA `0x32E7F40`.

## Event dispatch

The handler reads a 32-bit discriminator from the incoming event. It compares that value with storage at RVAs `0xB3BD070` and `0xB3BD074`. Static initialization at RVAs `0x331F48C` and `0x331F496` writes `0x60213267` and `0x5A1F5E67` to those locations.

The first match loads the published manager interface from corrected global RVA `0xB487020` and invokes vtable slot `+0x98` with Boolean `true`. That slot resolves to the already mapped mode-aware notification/state handler at RVA `0x33299F0`.

The second match loads the same interface and invokes slot `+0xA0`, RVA `0x332A1D0`. This small method checks manager helper pointer `+0x180` and clears helper byte `+0x1C` when the helper exists.

## Interpretation boundary

This is a real component-to-manager control edge and additional independent evidence for global RVA `0xB487020`. It is not yet evidence that either discriminator means “open photo camera,” “close photo camera,” or “enter FreePhoto.” The separate `RequestClosePhotoCamera` operation name and `sta_open_photomode` string are not assigned to these values without a registration or producer cross-reference. Runtime ordering and callback-thread identity remain unknown.
