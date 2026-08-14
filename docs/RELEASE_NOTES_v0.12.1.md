# v0.12.1 — DX11 Manager Global Correction

This corrective release changes the fingerprinted DX11 photo-camera manager-interface global from RVA `0xB486020` to `0xB487020`.

The corrected address is established independently by the startup publication store at RVA `0x321A5DA` and by numerous ordinary consumers, including the native event activation path and photo-camera listener. The previous value was an arithmetic transcription error.

The query/read-only observer and all current database/documentation references now use `0xB487020`. DX12 remains `0xB51C060` and is unaffected.

No activation code is included. Runtime lifecycle validation remains required before companion integration.
