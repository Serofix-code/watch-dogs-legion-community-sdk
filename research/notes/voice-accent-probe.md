# Voice/accent probe (static evidence pass)

## Result

The current evidence does **not** identify a standalone country-accent field. The operator data exposes several voice-related candidates:

The strongest new lead is the discovered runtime symbol `ChangePlayerGkModelFromHumanConfigAndVoiceActor`. It explicitly accepts a `HUMAN_CONFIG` and a `VOICE_ACTOR` resource, which is a better path for testing alternate voice banks than directly editing the 8-byte pitch/modulation profile. Its resource formats, argument ABI, thread affinity, and relationship to persistent operative data remain unresolved.

A read-only ASCII scan of the installed DX11 module also found the engine type/category string `tagcategoryNPCVoiceTagCategory`. This confirms that NPC voice tags exist as an engine tag category, but the scan did not expose individual accent names or a safe public enumeration function. It is a promising route for the next tag-database probe, not a writable offset.

The public tag catalog does expose six `Accent.*` tags and six `NPCVoice.FP_*` tags. These are now shown in the companion's read-only Voice Tags research window. Their relationship to the 4-byte persona field and 16-byte NPC voice-actor field is unresolved; the matching names must not be assumed to be interchangeable.

## Native string neighborhood (DX11 build)

The two native names occur at module string RVAs `0x0A11DFB8` and `0x0A11DFE8`. Nearby registered names include `ChangePlayerGkModelFromHumanConfig`, `AddPlayerTag`, `RemovePlayerTag`, `HasPlayerTag`, `TeleportEntity`, and `GetLocalCameraId`. This is useful call-site context, but these are string locations—not function entry points—and must not be patched or called as addresses.

| Candidate | Observed size/role | Interpretation | Confidence |
| --- | --- | --- | --- |
| Player Voice Actor / Persona | 4 bytes | active operative voice/persona selection | STRONGLY INFERRED |
| Voice Profile | 8 bytes | pitch, volume, and modulation profile | CONFIRMED by the table label; not a country selector |
| NPC Voice Actor | 16 bytes | emote/inactive-operative voice actor mask | STRONGLY INFERRED |
| Character Deck ID | 8 bytes | archetype/deck that can influence abilities and presentation | INFERRED; do not treat as accent alone |
| Recent birthplace events | event IDs | city/country and cultural biography (for example Jamaican birthplace events) | CONFIRMED as biography, not proof of spoken accent |

The table/configuration labels explicitly describe Voice Profile as pitch/volume/modulation and do not label it as nationality or accent. Jamaican, French, British, and similar labels observed in the data are predominantly birthplace/cultural events, name filters, or other metadata. A safe editor therefore presents these voice/persona candidates separately and does not silently map a birthplace to an accent.

## Runtime probe plan

1. Read the four candidate fields for the same operative before and after changing only the in-game voice/persona or voice-related state.
2. Require a stable pointer chain and repeat the read across several frames.
3. Correlate an observed voice change with exactly one field changing; treat simultaneous changes as unresolved.
4. Do not write a new value until a candidate is uniquely correlated and the build/signature is validated.

## New lead to probe

Search the live Lua/native inventory for `ChangePlayerGkModelFromHumanConfigAndVoiceActor` and its `_v1` variant. First perform a read-only symbol/string/xref scan, then identify valid voice-actor resource names from the engine-owned catalog. Do not pass guessed strings or a birthplace ID: an invalid resource can replace the player model or crash the session.

This is a read-only research result. No new memory-write offset is claimed here.
