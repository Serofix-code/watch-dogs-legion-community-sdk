# v0.9.1 — Runtime Helper Lifecycle

This release maps the engine-owned runtime helper created by `CPhotoCameraManager` setup and extends the read-only observer for targeted lifecycle validation.

## New evidence

- helper object size `0x160`, constructor RVA `0x3333170`, and type table RVA `0xA116FC0`;
- setup-owned mode and initialization paths at RVAs `0x3327130` and `0x33271E0`;
- selected mode, input/context pointers, event subscription, and three transition-token fields;
- ordered cleanup RVA `0x33279A0`, called before outer teardown nulls and deletes the helper;
- distinct adjacent type labels for the outer `CPhotoCameraManager` and inner `PhotoCameraManager` runtime helper.

The database contains 47 evidence records after this release.

## Read-only observer

When interface `+0x318` is non-null, `observe_photo_camera.py` now validates the exact helper type table and reports its selected mode, input/context pointers, event subscription, mode-registration state, and transition tokens. It still requests query/read access only and performs no allocation, injection, hook, suspension, protection change, or write.

## Limitations

The game was not running during this static pass. Runtime thread identity, service results, component creation, orientation axis order, and interruption/teardown behavior remain unverified. Companion activation therefore remains under development.
