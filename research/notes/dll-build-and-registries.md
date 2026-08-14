# DX11 module build identity and mission-symbol cluster

Read-only inspection of the locally installed Steam DX11 module was performed on 2026-08-14. No game binary or bulk string dump is included.

## Exact build fingerprint

- Module: `DuniaDemo_clang_64_dx11.dll`
- SHA-256: `086968CD9EC4D5939248846EAFA2DA72210FDDEB1164E79CBD08164313A0086E`
- Image base: `0x180000000`
- Image size: `0x22A0B000`
- PE timestamp: `0x653939C5` (2023-10-25 17:52:37 UTC)
- Embedded changelist: `2073645`
- Embedded branch: `//wd3-prod/milestone`
- Embedded milestone: `orwell-game-milestone-121`
- Embedded Uplay product: `7017`
- Embedded build date: `2023-10-04 17:48:00`
- Embedded target: `master`

The PE export table identifies 356 named exports and uses the internal module label `DuniaDemo_clang_64_dx11_steam_denuvo.dll`. Most visible exports are Wwise/AK interfaces; the research database does not treat those third-party exports as Legion SDK discoveries.

## Domino mission-operation cluster

A contiguous string cluster at file offsets `0xA382508` through `0xA3833E9` (RVAs `0xA383108` through `0xA383FE9`) starts with Domino controller names and then lists mission-facing operations. Relevant new names include:

- `AddRecruitNPCListener_v3`, `AddPredefinedOperative`, `RemoveRecruitNPCListener`
- `ForceLeverageNPC`, `ForceLeverageOnNextActorWithTag`, `RemoveEntityFromContactList`
- `GetOperativeIDList`, `_v2`, `_v3`, and `GetGameStartOperativesList`
- `GetOperativeBySlotNumber`, `GetCurrentOperative`
- `SetOperativeAvailable`, `SetOperativeUnavailable`
- `OverrideOperativeScheduleToCityLocation`, `CancelOperativeScheduleOverride`
- `RecruitmentIntelActivate`, `RecruitmentIntelGetEntity`
- `GetRuleSmithFloat`, `GetRuleSmithBool`, `GetRuleSmithInt`, `TriggerRuleSmithRule`

The same cluster also names objective, checkpoint, persistence, reinforcement, mission-waypoint, census-listener, drone, and scripted-hack operations. One member, `TriggerRuleSmithRule`, was independently observed through the game-thread Lua bridge. That cross-reference makes a scripting-registration interpretation likely, but it does not prove that every adjacent name has the same exposure mechanism.

Signatures, parameters, return types, registration descriptors, and safe call paths remain unknown. The records therefore preserve the exact names while classifying their behavior as inferred and unresolved.
