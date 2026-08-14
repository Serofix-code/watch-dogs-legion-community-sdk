from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


def _strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from _strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _strings(child)


@dataclass(frozen=True)
class ResearchRecord:
    data: dict[str, Any]
    source: Path

    @property
    def id(self) -> str:
        return str(self.data["id"])

    @property
    def name(self) -> str:
        return str(self.data["name"])

    @property
    def summary(self) -> str:
        return str(self.data["summary"])

    @property
    def confidence(self) -> str:
        return str(self.data["confidence"])

    @property
    def kind(self) -> str:
        return str(self.data["kind"])

    def matches(self, terms: Iterable[str]) -> bool:
        haystack = " ".join(_strings(self.data)).casefold()
        return all(term.casefold() in haystack for term in terms)


class ResearchDatabase:
    def __init__(self, records: Iterable[ResearchRecord]):
        self.records = tuple(records)
        self._by_id = {record.id: record for record in self.records}

    @classmethod
    def open_repository(cls, root: str | Path) -> "ResearchDatabase":
        directory = Path(root).resolve() / "database" / "records"
        records: list[ResearchRecord] = []
        for path in sorted(directory.glob("*.json")):
            with path.open("r", encoding="utf-8-sig") as stream:
                values = json.load(stream)
            if not isinstance(values, list):
                raise ValueError(f"{path} must contain a JSON array")
            records.extend(ResearchRecord(dict(value), path) for value in values)
        return cls(records)

    def get(self, identifier: str) -> ResearchRecord | None:
        return self._by_id.get(identifier)

    def search(self, query: str) -> tuple[ResearchRecord, ...]:
        terms = query.split()
        return tuple(record for record in self.records if record.matches(terms))
