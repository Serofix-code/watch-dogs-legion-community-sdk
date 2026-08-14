# Photo-camera configuration discovery

Read-only string and PE-section inspection of the exact Steam DX11 module found a dense reflected configuration cluster beginning with `PhotoCameraConfig` at file offset `0x9E9E0E8` (RVA `0x9E9ECE8`).

The cluster names input/action concepts including `ToggleEditMode`, `SwitchMode`, `TakePicture`, `Focus`, `ZoomStart`, `ZoomEnd`, `ChangeAngleStart`, `ResetSettings`, `ResetCamera`, and `ResetScene`. It also describes lens/sensor defaults, availability timers, selfie offsets, focal-length search behavior, photo menu categories, adjustable values, and cinematic availability.

Most importantly, it contains `FreeModeCamera` at file offset `0x9E9E2A8` (RVA `0x9E9EEA8`), immediately followed by enter and movement-start/end concepts. This is new evidence that Legion's built-in photo-camera subsystem has an explicit free-movement mode. It does **not** yet reveal the controller instance, numeric enum value, input dispatcher, transform, or activation call.

This finding changes the freecam research direction: locating the `PhotoCameraConfig` type descriptor, its mode-selection consumer, and the controller that handles `MovementStart`/`MovementEnd` is likely more precise than another global unknown-float scan.
