# Smartphone Lua binding-name family

This note records static, read-only string-corpus analysis of the exact Steam DX11 and DX12 modules listed in `docs/BUILDS.md`.

## Cross-renderer family

Both modules contain the same contiguous sequence of ten callable-style names:

1. `SmartphoneActivateOverride`
2. `SmartphoneClearOverride`
3. `SmartphoneAppSetHidden`
4. `SmartphoneAppSetNew`
5. `SmartphoneAppSetAvailable`
6. `SmartphoneAppSetInstalled`
7. `SmartphoneIsAppInstalled`
8. `SmartphoneIsOpened`
9. `SmartphoneIsAppOpened`
10. `SmartphoneGetAppId`

The family spans DX11 RVA `0xA11F87F` through `0xA11F953` and DX12 RVA `0xA1AEABF` through `0xA1AEB93`. Ordering and spelling are identical across the fingerprinted renderers.

The names occur inside the broader native Lua-binding corpus beside other known callable gameplay operations. That supports classifying them as a binding family, but static name presence alone does not establish parameter types, return types, thread affinity, or whether every binding remains enabled in the shipping runtime.

## FreePhoto relevance

The independently mapped phone/application enum assigns `PhotoCamera` value `16`. `SmartphoneGetAppId` and `SmartphoneActivateOverride` therefore form a plausible app-level research direction, potentially safer than directly calling manager setup or writing camera-component state.

This relationship is only a hypothesis. No registration wrapper, argument decoder, accepted application-name representation, override owner, clear/close ordering, or runtime result has been established. The companion must not call these bindings until their signature and cleanup behavior are validated on an engine-owned game thread.
