# Player and waypoint coordinate research

Observed on Steam PC DX11 on 2026-08-14.

Three guarded capture sites produced an active-player owner, its coordinate object, and the current map waypoint. Filtering the coordinate writer by the captured active-player owner avoided selecting unrelated world objects.

The player coordinate object stores floats at `+0x80`, `+0x84`, and `+0x88`. The verified human-facing mapping is:

- X = `+0x80`
- elevation = `+0x88`
- the other horizontal axis = `+0x84`

The map waypoint path reads a nested object at source `+0x18`, then components at `+0x70`, `+0x78`, and `+0x74`. A non-zero captured waypoint was used successfully by the observed teleport path.

Safe write experiments stored the complete pre-write player position before changing the first float, suspended remote threads for the three-component update, read the result back, and kept a bounded recovery history. This establishes the observed layout, not collision safety, world bounds, or a general-purpose transform API.

True freecam remains separate and unresolved: the player transform is not evidence of a camera transform.
