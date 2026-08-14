# v0.10.1 — Orientation Mapping Correction

This corrective release replaces the preliminary v0.10.0 orientation label with a mapping supported by reflected field names and native data flow.

## Correct mapping

| Component offset | Angle |
| --- | --- |
| `+0x70` | pitch |
| `+0x74` | roll |
| `+0x78` | yaw |

## Evidence

- `fPitchRotationSpeed` is registered at `+0x1D8`, updates accumulator `+0x1BC`, and uses pitch limits `+0x1C8/+0x1CC`;
- `fRollRotationSpeed` is registered at `+0x1E0`, updates accumulator `+0x1C0`, and uses roll limits `+0x1D0/+0x1D4`;
- `fYawRotationSpeed` is registered at `+0x1DC` and updates accumulator `+0x1C4`;
- initialization copies `+0x1BC/+0x1C0/+0x1C4` to `+0x70/+0x74/+0x78` in that order;
- RVA `0x323AA10` rebuilds the same three Euler fields from the component quaternion.

The read-only observer, database, current research note, README, progress report, changelog, and v0.10.0 release note are corrected. Runtime sign/direction conventions still require observation. No companion activation code is included.
