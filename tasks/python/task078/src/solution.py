from __future__ import annotations

from collections import defaultdict


class MemDB:
    def __init__(self) -> None:
        self._tables: dict[str, list[dict]] = defaultdict(list)

    def insert(self, table: str, row: dict) -> None:
        self._tables[table].append(dict(row))

    def find(self, table: str, **filters) -> list[dict]:
        rows = self._tables.get(table, [])
        return [r for r in rows if all(r.get(k) == v for k, v in filters.items())]

    def delete(self, table: str, **filters) -> int:
        before = self._tables.get(table, [])
        if not filters:
            count = len(before)
            self._tables[table] = []
            return count
        kept = [r for r in before if not all(r.get(k) == v for k, v in filters.items())]
        removed = len(before) - len(kept)
        self._tables[table] = kept
        return removed
