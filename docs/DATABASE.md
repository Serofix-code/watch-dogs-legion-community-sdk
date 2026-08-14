# Database format

Research records live in `database/records/*.json` and validate against `database/schemas/research-record.schema.json`. Required fields include stable ID, kind, summary, confidence, status, build observations, and evidence.

Related symbols use stable IDs. Evidence references point to non-proprietary repository notes. Generated indexes are deterministic and checked in CI.
