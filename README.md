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

Read-only local binary research is supported without creating a string dump:

```bash
python tools/inspect_binary_strings.py path/to/module.dll --contains PhotoCamera --contains FreeModeCamera --max-results 100
```

The inspector requires explicit filters, caps output, and never writes extracted data. See [docs/BINARY_RESEARCH.md](docs/BINARY_RESEARCH.md).

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
- an exact Steam DX11 build fingerprint and embedded product-version identity;
- a newly discovered Domino mission-operation cluster covering recruitment, operative availability, schedules, objectives, and persistence;
- the built-in `CPhotoCameraConfig`, `CCameraFreePhotoComponent`, and `CPhotoCameraManager` runtime path;
- the free-photo-camera position/orientation layout and native transform update path;
- guarded signatures and build-specific offsets;
- negative reward and camera experiments, including why their apparent acknowledgements were insufficient.

The native free-photo-camera component and transform are mapped statically, together with the manager's guarded setup, teardown, requested-state wrapper, native mode-5 dispatch, and dedicated action-map selection. Public activation remains under development because manager lifetime, the game-thread contract, orientation order, and interrupted teardown still require runtime validation. The earlier automatic calibration experiment is retained as useful negative evidence.

See [RESEARCH_PROGRESS.md](RESEARCH_PROGRESS.md) and the [generated research index](docs/generated/RESEARCH_INDEX.md).

## Build compatibility

Current observations target Steam PC DX11 changelist `2073645`, milestone `orwell-game-milestone-121`. The exact `DuniaDemo_clang_64_dx11.dll` SHA-256 is `086968CD9EC4D5939248846EAFA2DA72210FDDEB1164E79CBD08164313A0086E`. Compatibility with other distributions, renderers, or updates is **unknown**. Never upload a game module; submit only its digest and independently written evidence.

## Contributing

Use the discovery template under `research/templates/`, retain honest unknowns, add non-proprietary evidence, and run every validator. Corrections are as valuable as new symbols. Read [CONTRIBUTING.md](CONTRIBUTING.md).

## License

The independently created code and documentation in this repository are available under the [MIT License](LICENSE). This license does not grant rights to Ubisoft material or third-party content.
