# Build compatibility

## Steam Windows x64 DX11 — changelist 2073645

- Module: `DuniaDemo_clang_64_dx11.dll`
- SHA-256: `086968CD9EC4D5939248846EAFA2DA72210FDDEB1164E79CBD08164313A0086E`
- Internal milestone: `orwell-game-milestone-121`
- Branch: `//wd3-prod/milestone`
- Embedded build date: 2023-10-04 17:48:00
- PE timestamp: 2023-10-25 17:52:37 UTC
- Observed locally: 2026-08-14

## Steam Windows x64 DX12 — changelist 2073645

- Module: `DuniaDemo_clang_64_dx12.dll`
- SHA-256: `E37381D67A7D7CDA377A90B05793E897A0D7321D1C568AD09C5882481AAC9EB6`
- Internal milestone: `orwell-game-milestone-121`
- Branch: `//wd3-prod/milestone`
- PE timestamp: 2023-10-25 16:09:16 UTC
- Observed locally: 2026-08-14

The FreePhoto camera layout and lifecycle have been mapped statically in both modules. Runtime validation remains outstanding, and offsets/action identifiers are renderer-specific. Other stores and patches remain unknown. Submit module hashes only—never game modules.
