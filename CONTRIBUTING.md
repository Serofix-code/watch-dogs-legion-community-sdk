# Contributing

## Research integrity

- Use single-player/offline builds only. Multiplayer abuse and anti-cheat bypasses are out of scope.
- Never upload Ubisoft executables, DLLs, assets, source/decompilation dumps, saves, credentials, personal data, or unredacted crash dumps.
- Record `unknown` instead of guessing a signature, return type, calling convention, or ownership rule.
- Identify platform, distribution, module, observation date, and module SHA-256 when available.
- A confidence promotion to `confirmed` requires reproducible direct evidence on a named build.

## Submission workflow

1. Copy `research/templates/discovery.example.json`.
2. Add a stable namespaced record under `database/records/`.
3. Add longer non-proprietary notes under `research/notes/` when needed.
4. Run:

   ```bash
   python tools/validate_database.py
   python tools/check_duplicate_symbols.py
   python tools/check_broken_references.py
   python tools/generate_docs.py --check
   python -m unittest discover -s tests
   ```

5. Open a pull request explaining observed behavior, confidence, build compatibility, and remaining unknowns.

Incorrect discoveries can be reported without proposing a replacement theory.
