# Voice/accent probe (static evidence pass)

## Result

The current evidence does **not** identify a standalone country-accent field. The operator data exposes several voice-related candidates:

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

This is a read-only research result. No new memory-write offset is claimed here.
