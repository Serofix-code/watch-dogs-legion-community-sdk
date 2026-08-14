# Registered photo-camera close command

This note records static, read-only analysis of the registered `RequestClosePhotoCamera` command in the exact Steam DX11 and DX12 modules listed in `docs/BUILDS.md`.

## Registry association

The command string is constructed during the same generated static-initialization sequence as adjacent named operations. In that sequence, the command is paired with these wrapper functions:

- DX11 wrapper RVA `0x4247C90`;
- DX12 wrapper RVA `0x4247EE0`.

The wrappers use the engine's command-argument reader, require an argument count of zero, return false for a mismatched invocation, and otherwise call a dedicated emitter before returning true.

## Event emission

The emitters are DX11 RVA `0x4245C40` and DX12 RVA `0x4245E90`. Each performs the same operations:

1. allocate a `0x18`-byte event object;
2. run the common event-object constructor;
3. install the build-specific event vtable;
4. lazily resolve the build-specific event-channel singleton;
5. submit the owned event through the engine's channel dispatch routine.

Observed event and channel locations are:

| Build | Event vtable RVA | Channel global RVA |
| --- | ---: | ---: |
| DX11 | `0xA124760` | `0xB298D30` |
| DX12 | `0xA1B37A0` | `0xB32DD30` |

The adjacent reflected type name `CPhotoCameraEventChannel` strongly supports the photo-camera channel interpretation, but the formal source-level event payload type remains unresolved. The emitted object carries no command arguments.

## Lifecycle consequence

The registered close operation uses engine-owned event dispatch instead of directly invoking manager teardown. This supplies a documented safe-lifecycle direction for future runtime work, but the command registry invocation API, dispatch thread, acknowledgement, and interruption behavior are not yet mapped. No matching registered open command was found, so this does not provide a complete external FreePhoto activation recipe.
