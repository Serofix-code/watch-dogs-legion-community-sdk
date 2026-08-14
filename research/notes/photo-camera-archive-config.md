# Photo-camera archive configuration

This note records a bounded, read-only inspection of `common.fat` / `common.dat` from the observed Steam installation. The FAT index SHA-256 is `9DC03F7F06FDC6CCB06A871B5589565FD324BF93B30F674C3DD7A43186AA9614`. Extracted Ubisoft objects and generated XML are **not** included in this repository.

## Reproducible FAT5 facts

The open-source [Gibbed Disrupt implementation](https://github.com/gibbed/Gibbed.Disrupt/tree/8c41fe50fabf2eb5673919ef6b5fff1c09186381) establishes WDL's FAT5 version-13 entry layout and name-hash algorithm. The focused local inspector confirms these named entries in `common.fat`:

| Entry | Name hash | Compressed | Decoded | Scheme | Decoded SHA-256 |
| --- | --- | ---: | ---: | ---: | --- |
| `generated\\databases\\generic\\photocameraconfig_40469731.obj` | `A27499A333E8AA3E` | `0x4B1` | `0x6D7` | `3` | `B9C3A354511FAC3CE372F2B1CD193AEA68BBEF41F643372AED136BE6758820E6` |
| `generated\\databases\\generic\\photocameramenucategories.lib` | `A3A63261572FB87E` | `0x30A` | `0x8D2` | `3` | `ADBA5CF4F60C7651B0EC1D9010FA557C1B5122E9BD28A2214FA6F7390502A6C5` |
| `generated\\databases\\generic\\photocameramenuitems.lib` | `AEDA7E05558E7978` | `0x1305` | `0x422C` | `3` | `2DCDCBC6A4D598693FFCC508F08711E3F6B8B8B96EE00E2185BEE23B85D27979` |

For all three observed scheme-3 entries, the first byte is a wrapper byte and the remainder is a standard raw LZ4 block. This observation is intentionally limited to these records; it is not yet claimed for every WDL scheme-3 entry.

## Mode values and bounded configuration facts

Structured conversion with the pinned public WDL class definitions identifies these photo-camera mode values:

| Value | Configured mode |
| ---: | --- |
| `0` | Normal |
| `1` | Selfie |
| `5` | FreePhoto |
| `6` | PhotoBooth |

Mode value `3` occurs in shared menu-item availability lists, but its name is unresolved. No names are fabricated for values `2`, `3`, or `4`.

The `FOV.FreePhoto` menu item is explicitly limited to mode `5`, is player-editable, uses the game camera default, and has a configured range of `45` to `90`. The main config resets the photo-camera mode when reopened. It also contains the `FreeModeCamera` enter, exit, movement-start, and movement-end groups observed in the reflected DLL registration.

These configuration records corroborate the native free-mode route but do not establish its game-thread calling contract or prove that mode value `5` can be forced safely from an external process.
