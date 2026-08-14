# Gameplay camera component leads

This note documents bounded, read-only string-corpus evidence from the exact Steam PC renderer modules listed in `docs/BUILDS.md`. It does not establish a callable API, a live object, or a safe write path.

## CCameraComponent

The DX11 module contains `CCameraComponent` at file offset `0xA3F3753` and a generated `UTDS::xxxUpdate` registration literal at `0xA3FC9E0`. The matching DX12 module contains the same class name at `0xA482663` and the generated update literal at `0xA48B8F0`.

This is the broad camera-component lead. The active scene-camera instance, vtable, object size, transform fields, and whether it is attached to the normal operative camera have not been established.

## CCameraGameProcessingComponent

The DX11 module contains `CCameraGameProcessingComponent` at `0x9F5C68A`, with named methods for pre-physics update, visibility tests, aiming-assistance tests, Z-lock, gaze-to-object raycasts, reticle-hit raycasts, and target lock. Its generated update-registration literals name four phases:

- `UpdatePrePhysics` at `0x9F5FD10`;
- `UpdatePostInput` at `0x9F5FD90`;
- `UpdatePostPhysics` at `0x9F5FE0F`;
- `UpdatePostCamera` at `0x9F5FE90`.

The names strongly support a gameplay-facing camera-processing role. They do not prove this component stores or writes the normal scene-camera transform.

## CCameraFreeComponent

Both exact renderer modules contain a component named `CCameraFreeComponent` with a generated `UTDS::xxxUpdate` registration, separate from `CCameraFreePhotoComponent` and `CPhotoCameraManager`:

| Renderer | Component marker | Update registration literal |
|---|---:|---:|
| DX11 | `@CameraFreeComponent` at `0xA47DD37` | `CCameraFreeComponent, xxxB = UTDS::xxxUpdate` at `0xA481A50` |
| DX12 | `@CameraFreeComponent` at `0xA50CBC7` | `CCameraFreeComponent, xxxB = UTDS::xxxUpdate` at `0xA5108E0` |

This is a strong research lead for an independent gameplay free camera because it is named separately from the validated Photo Mode route. It is not evidence that the component is instantiated in normal Story Mode, that it is reachable externally, or that it can safely replace the operative-follow camera.

### Reflected configuration surface

The contiguous DX11 `CameraFreeComponent` parameter corpus starts at `0xA47DD37`. It names a `CameraContext`, `UpdateParameters`, FOV controls, pitch/yaw input controls, rotation constraints, following, pivoting, collision, ideal offsets, reticle placement, lens settings, and blending. In particular, it includes:

- `fInputYawSpeed` and `fInputPitchSpeed`;
- `selRotationReference`, yaw/pitch offsets, and yaw/roll/pitch bounds;
- `bFollowPitch`, `bFollowYaw`, follow references, follow lag, follow delay, and follow speed thresholds;
- pivot reference, pivot lag, pivot offsets, and optional female pivot offset;
- collision radius/frustum radius/lag controls;
- ideal camera offsets for left/right/front/back;
- FOV interpolation, FOV acceleration, and FOV limits.

The matching DX12 corpus includes `fFollowPYLag` at `0xA50CFE4`, in addition to the `CCameraFreeComponent` marker and update registration. These fields strongly support the interpretation that this component controls a normal player-following camera. The layout, runtime field offsets, and owning instance are still unknown.

## Next evidence required

1. Recover the component's vtable, object size, and constructor/destructor from its reflection registration.
2. Locate a live normal-gameplay instance using exact-vtable validation only.
3. Read-only verify candidate transform, orientation, FOV, and input fields while the operative remains stationary.
4. Trace the per-frame writer and owner edge that follows the operative.
5. Establish an engine-thread activation and cleanup path before adding any camera write to the companion.
