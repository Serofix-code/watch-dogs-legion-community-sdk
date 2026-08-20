# French VO trace attempt

The supplied `WDL_FrenchVO_broad_trace.txt` and `WDL_FrenchVO_dialogue_trace.txt` were reviewed.
They installed wrappers for 61 candidate Lua/table methods, including
`CDominoSoundManager.PlayDialogWithSubtitle(_v2/_v3)`, `PlaySound(_v2)`, and
`CGameplayConversationManager` conversation methods. The traces stayed at `calls=0` while the
player changed operatives and were then uninstalled.

This is useful negative evidence: those Lua-visible wrappers are not the live procedural speech
boundary for normal operative barks, or the test did not exercise a matching conversation path.
They cannot be used as the French per-operative switch by themselves.

The next safe target remains the native Wwise `PostEvent`/dialogue boundary. It must be observed
read-only with event ID, game-object ID, and current entity ID before any French bank routing is
attempted. No memory write or global language change is claimed by this result.
