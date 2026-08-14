# v0.13.0 — Photo-camera Component Bridge

This release maps an ordinary `CPhotoCameraComponent` event path into the native photo-camera manager.

## New map

- `CPhotoCameraComponent` constructor and its two native vtable regions;
- event-handler RVA `0x32E7F40`;
- opaque discriminator values `0x60213267` and `0x5A1F5E67` plus their static initializer;
- first branch to manager slot `+0x98`, the mode-aware notification/state handler;
- second branch to manager slot `+0xA0`, which clears helper byte `+0x1C`.

This also supplies another independent ordinary consumer of the corrected DX11 manager global RVA `0xB487020`.

## Remaining boundary

The discriminator names, event producer, callback thread, and relationship to app-level open/close requests remain unknown. Neither discriminator is labeled as “open,” “close,” or “FreePhoto activation” without direct evidence. No companion activation code is included.
