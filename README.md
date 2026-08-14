# Watch Dogs: Legion Community SDK

[![Validate](https://github.com/Serofix-code/watch-dogs-legion-community-sdk/actions/workflows/validate.yml/badge.svg)](https://github.com/Serofix-code/watch-dogs-legion-community-sdk/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An unofficial, open-source, evidence-first SDK reference and reverse-engineering database for the single-player/offline PC version of *Watch Dogs: Legion*.

This project is not affiliated with, authorized by, or endorsed by Ubisoft. *Watch Dogs*, *Watch Dogs: Legion*, Ubisoft, and related names are trademarks of their respective owners. The repository contains independently written tools and factual interoperability research—not game binaries, proprietary source code, copyrighted game assets, saves, credentials, or anti-cheat bypasses.

## Status and confidence

| Level | Meaning |
|---|---|
| **CONFIRMED** | Reproduced on a named build with direct evidence and validation. |
| **STRONGLY INFERRED** | Multiple observations agree, but an important contract remains incomplete. |
| **INFERRED** | Plausible from limited evidence; do not treat as stable API. |
| **UNKNOWN** | Purpose, signature, layout, compatibility, or behavior remains unresolved. |

Confidence is build-specific and does not imply that a write is safe.

## Repository layout

```text
database/   Machine-readable research records and schemas
docs/       Human-readable reference and GitHub Pages site
sdk/        Reusable SDK readers and future stable interfaces
tools/      Validation, duplicate, reference, query, and generation tools
examples/   Game-file-free usage examples
research/   Evidence notes, failed experiments, and submission templates
```

## Search

No installation is required for the command-line tools beyond Python 3.11+.

```bash
python tools/query_database.py "operative roster"
python tools/query_database.py camera
python tools/validate_database.py
python tools/check_duplicate_symbols.py
python tools/check_broken_references.py
python tools/generate_docs.py --check
```

Python SDK example:

```python
from pathlib import Path
import sys

sys.path.insert(0, str(Path("sdk/python").resolve()))
from wdl_sdk import ResearchDatabase

database = ResearchDatabase.open_repository(".")
for record in database.search("camera"):
    print(record.id, record.confidence, record.summary)
```

## Current coverage

The database currently documents:

- operative roster and census traversal;
- biography events, scalar statistics, packed appearance, perks, and contract schedules;
- an engine-thread Lua command bridge and observed entity/world bindings;
- active-player and map-waypoint coordinate capture;
- guarded signatures and build-specific offsets;
- negative reward and camera experiments, including why their apparent acknowledgements were insufficient.

True freecam remains unresolved. The completed automatic camera-calibration experiment is retained as negative evidence: forcing horizontal and vertical movement into one surviving scalar selected a continuously changing false positive rather than a validated camera transform.

See [RESEARCH_PROGRESS.md](RESEARCH_PROGRESS.md) and the [generated research index](docs/generated/RESEARCH_INDEX.md).

## Build compatibility

Current live observations are from the Steam PC DX11 module `DuniaDemo_clang_64_dx11.dll` in August 2026. Its exact module SHA-256 has not yet been recorded, so compatibility with other distributions, renderers, or updates is **unknown**. Never upload a game module; submit only its digest and independently written evidence.

## Contributing

Use the discovery template under `research/templates/`, retain honest unknowns, add non-proprietary evidence, and run every validator. Corrections are as valuable as new symbols. Read [CONTRIBUTING.md](CONTRIBUTING.md).

## License

The independently created code and documentation in this repository are available under the [MIT License](LICENSE). This license does not grant rights to Ubisoft material or third-party content.
