# Per-operative French voice status

## Confirmed local evidence

- The installed build contains `data_win64/sound_french.dat` and `.fat` plus
  `data_win64/worlds/london/london_sound_french.dat` and `.fat`.
- The audio discovery log reports `CDominoSoundManager` and
  `CGameplayConversationManager` as Lua tables. Their dialogue methods are present:
  `PlayDialogWithSubtitle`, `_v2`, `_v3`, `PlaySound`, `_v2`, and
  `PlayConvoFromLUA` / `PlayConvoOnEntityListFromLUA`.
- Exact global setters such as `SetVoiceLanguage`, `SetAudioLanguage`, and
  `SetCurrentLanguage` were not present. A global language switch therefore cannot
  be reused as a per-operative solution.
- The native journal has registration xrefs for the dialogue methods and decorated
  Wwise `AK::SoundEngine::LoadBank` and `PostEvent` symbols.

## What this means

The French audio assets exist, but the repository does not yet contain a validated
per-speaker routing mechanism. The French-influencer appearance resource is clothing/
model data, not proof of a French voice bank. The operative's persona and voice-profile
fields also do not identify a French language bank.

## Required next proof

1. Capture a read-only `PostEvent`/dialogue call boundary while the controlled operative
   speaks and record event ID, Wwise game-object ID, and current entity ID.
2. Repeat with an ordinary NPC and a second operative to prove the speaker discriminator.
3. Map the matching French event/bank pair and route only the controlled operative's
   game object, leaving subtitles and world/NPC language unchanged.

Until those three checks pass, a write or global language switch would change more than
the selected operative and could break audio or save/session state.
