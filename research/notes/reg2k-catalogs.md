# reg2k Watch Dogs: Legion reference catalogs

These catalogs are public, human-readable research references hosted by [reg2k's public gists](https://gist.github.com/reg2k). They are useful for resolving names and hashes in tools, but they are not an ABI or proof that a value is safe to write at runtime.

## Imported sources

| Catalog | Purpose | Confidence |
| --- | --- | --- |
| `wdl_perks.txt` | 8-character perk/ability IDs and internal names | STRONGLY INFERRED (name/hash catalog) |
| `wdl_tags.txt` | 64-bit tag IDs, decimal forms, and names | STRONGLY INFERRED (tag catalog) |
| `wdl_prismactorlist.txt` | Prism actor IDs and role labels | INFERRED (actor catalog) |
| `wdl_contracts_attendances.txt` | contract attendance identifiers | INFERRED (identifier catalog) |
| `wdl_clothing_*.txt` | clothing item identifiers grouped by garment type | INFERRED (catalog; ownership behavior not implied) |
| `wdl_character_models.txt` | character model identifiers | INFERRED (model catalog) |
| `wdl_characterdeck.txt` / `wdl_charactercard.txt` | character deck/card identifiers | INFERRED (catalog) |
| `wdl_profiler_metadata.txt` | profiler metadata identifiers and labels | INFERRED (metadata catalog) |
| `wdl_names.txt` / `wdl_surnames.txt` | localized name identifiers | INFERRED (name catalog) |
| `wdl_items_dump.txt` / `wdl_weapon_ability_ids.txt` | item and weapon ability identifiers | INFERRED (catalog) |

The importer in `tools/import_reg2k_gists.py` downloads the selected public files, preserves the source URL and retrieval time, and emits normalized JSON records. It deliberately does not scan or upload game binaries, save files, credentials, or Ubisoft assets.

## Runtime use

Catalog records should be used to improve display and search (for example, showing a readable perk name next to a hash). A catalog match alone must never be treated as permission to patch memory. Runtime writes remain build-gated, pointer-validated, reversible, and explicitly marked experimental in the companion/trainer UI.
