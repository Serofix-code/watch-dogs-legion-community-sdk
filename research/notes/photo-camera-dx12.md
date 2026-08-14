# DX12 photo-camera compatibility map

This note records static, read-only analysis of `DuniaDemo_clang_64_dx12.dll` with SHA-256 `E37381D67A7D7CDA377A90B05793E897A0D7321D1C568AD09C5882481AAC9EB6`. It contains changelist `2073645`, milestone `orwell-game-milestone-121`, and branch `//wd3-prod/milestone`, matching the product-version family of the fingerprinted Steam DX11 module. All RVAs below are specific to this exact DX12 module.

No game process was started for this work. The mapping is static compatibility evidence, not runtime confirmation and not an external activation recipe.

## FreePhoto component

The reflected `CCameraFreePhotoComponent` registration is present in DX12 with the same `0x410`-byte object layout as DX11. Its factory is at RVA `0x3239320`, constructor at `0x323A340`, destructor at `0x323A5A0`, and vtable at `0xA18B3C0`. The update callback at `0x323E060` calls transform routine `0x323CC90`; three direct callers reference that transform routine. Constructor code calls quaternion-to-Euler routine `0x323AC40`.

The reflection registrations independently encode pitch, yaw, and roll speed offsets `+0x1D8`, `+0x1DC`, and `+0x1E0`. The complete transform/input layout matches DX11: pitch/roll/yaw `+0x70/+0x74/+0x78`, position `+0x194`, accumulators `+0x1BC/+0x1C0/+0x1C4`, movement input `+0x21C`, and pitch/yaw/roll inputs `+0x234/+0x238/+0x23C`.

## Manager and helper lifecycle

Startup at RVA `0x321A770` allocates and constructs the outer manager at `0x3320760`. The interface subobject remains at `+0x2E8`, uses vtable RVA `0xA1A5C40`, and is published through global RVA `0xB51C060`.

The setup and teardown entries are `0x3326F90` and `0x3327670`. Setup creates the same `0x160`-byte runtime helper at interface `+0x318`; its constructor is `0x33333A0`, type table `0xA1A6000`, and delete thunk `0x346C380`. Setup calls the helper's set-mode entry `0x3327360` and initializer entry `0x3327410`.

Teardown directly proves the ordered cleanup contract. At `0x3327884` it loads helper `+0x318`, calls cleanup `0x3327BD0`, reloads the pointer, clears `+0x318`, and only then invokes the helper's virtual deleting destructor. Cleanup is a distinct function entry, not an address inferred only by a renderer-wide RVA delta.

The subscription table is at `0xA1A5FD0` with delete thunk `0x346C350`, dispatch thunk `0x3332AF0`, and state callback `0x33332C0`. Object size and owner back-pointer remain `0x10` and `+0x08`.

## Native activation chain

The DX12 event dispatcher is bounded by unwind metadata at `0x3332B00-0x33332B8`; its mode-5 branch begins at `0x3332EF0` and calls activation caller `0x3336470` from `0x3332F2C`. The callback entry is `0x33365F0`. The guarded free-mode wrapper is `0x33295E0`, with availability guard `0x33283C0`; it reaches internal free-mode toggle `0x3326C90` through interface slot `+0x28`.

The action-ID storage is RVA `0xB453FB4` and contains `0x5349BB24`. This differs from DX11's `0x81489DE8` even though both modules identify the same changelist. Action identifiers, published globals, vtables, and code RVAs must therefore be selected by exact module fingerprint; they are not renderer-independent constants.

## Compatibility conclusion

DX11 and DX12 share the camera object sizes, field offsets, interface-subobject offset, helper ownership model, mode value `5`, vtable slot meanings, and cleanup ordering. Their executable RVAs, globals, type tables, and raw action IDs differ. Runtime component creation, axis signs, callback thread, interruption behavior, and safe external activation remain unverified for both renderers.
