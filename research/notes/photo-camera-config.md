# Photo-camera configuration discovery

Read-only string and PE-section inspection of the exact Steam DX11 module found a dense reflected configuration cluster beginning with `PhotoCameraConfig` at file offset `0x9E9E0E8` (RVA `0x9E9ECE8`).

The cluster names input/action concepts including `ToggleEditMode`, `SwitchMode`, `TakePicture`, `Focus`, `ZoomStart`, `ZoomEnd`, `ChangeAngleStart`, `ResetSettings`, `ResetCamera`, and `ResetScene`. It also describes lens/sensor defaults, availability timers, selfie offsets, focal-length search behavior, photo menu categories, adjustable values, and cinematic availability.

Most importantly, it contains `FreeModeCamera` at file offset `0x9E9E2A8` (RVA `0x9E9EEA8`), immediately followed by `sndEnter`, `sndMovementStart`, `sndMovementEnd`, `MovementStart`, and `MovementEnd`. Subsequent reflection and factory tracing corrects the initial classification: `FreeModeCamera` is a configuration subsection heading, **not** a numeric enum value.

For the observed module, `CPhotoCameraConfig` has constructor RVA `0xE7E5B0`, destructor RVA `0xE7EFF0`, vtable RVA `0x9E9F400`, and object size `0x320`. Its factory at RVA `0x327EC20` allocates that exact size and invokes the constructor. The registration path associates the config factory with the `CCameraFreePhotoComponent` factory at RVA `0x32390F0`.

The component and runtime transform are documented in [photo-camera-runtime.md](photo-camera-runtime.md). A safe public activation call remains unresolved.
