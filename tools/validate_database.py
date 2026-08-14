from __future__ import annotations

import re
import sys
from datetime import date

from common import load_records

KINDS = {"build", "function", "event", "lua_api", "command", "ui", "type", "enum", "hash", "system", "signature", "offset", "call_chain"}
CONFIDENCE = {"confirmed", "strongly_inferred", "inferred", "unknown"}
STATUS = {"usable", "experimental", "under_development", "unresolved", "deprecated"}
EVIDENCE = {"runtime_observation", "signature_scan", "readback", "call_site", "string_reference", "cross_reference", "negative_result", "unknown"}
ID = re.compile(r"^[a-z0-9]+(?:[._-][a-z0-9]+)+$")
SHA256 = re.compile(r"^[A-Fa-f0-9]{64}$")
REQUIRED = {"id", "kind", "name", "summary", "confidence", "status", "builds", "evidence"}


def validate() -> list[str]:
    errors: list[str] = []
    for record in load_records():
        label = f"{record['_source']}:{record.get('id', '<missing>')}"
        missing = REQUIRED - record.keys()
        if missing:
            errors.append(f"{label}: missing {', '.join(sorted(missing))}")
        if not ID.fullmatch(str(record.get("id", ""))):
            errors.append(f"{label}: invalid id")
        if record.get("kind") not in KINDS:
            errors.append(f"{label}: invalid kind")
        if record.get("confidence") not in CONFIDENCE:
            errors.append(f"{label}: invalid confidence")
        if record.get("status") not in STATUS:
            errors.append(f"{label}: invalid status")
        builds = record.get("builds")
        if not isinstance(builds, list) or not builds:
            errors.append(f"{label}: builds must be non-empty")
        else:
            for index, build in enumerate(builds):
                try:
                    date.fromisoformat(str(build.get("observed", "")))
                except ValueError:
                    errors.append(f"{label}: build {index} has invalid date")
                digest = build.get("moduleSha256")
                if digest is not None and not SHA256.fullmatch(str(digest)):
                    errors.append(f"{label}: build {index} has invalid SHA-256")
        evidence = record.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{label}: evidence must be non-empty")
        else:
            for index, item in enumerate(evidence):
                if item.get("type") not in EVIDENCE or not item.get("reference") or not item.get("notes"):
                    errors.append(f"{label}: evidence {index} is malformed")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print(f"Database validation passed: {len(load_records())} records.")
