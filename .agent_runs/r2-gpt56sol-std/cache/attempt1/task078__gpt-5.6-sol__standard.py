from __future__ import annotations

from typing import Any


class MemDB:
    """A simple in-memory database organized into named tables."""

    def __init__(self) -> None:
        self._tables: dict[str, list[dict[str, Any]]] = {}

    def insert(self, table: str, row: dict[str, Any]) -> None:
        """Insert a row into a table."""
        self._tables.setdefault(table, []).append(dict(row))

    def find(self, table: str, **filters: Any) -> list[dict[str, Any]]:
        """Return rows matching all supplied filters."""
        rows = self._tables.get(table, [])
        return [
            dict(row)
            for row in rows
            if all(key in row and row[key] == value for key, value in filters.items())
        ]

    def delete(self, table: str, **filters: Any) -> int:
        """Delete rows matching all supplied filters and return their count."""
        rows = self._tables.get(table)
        if not rows:
            return 0

        remaining: list[dict[str, Any]] = []
        deleted = 0

        for row in rows:
            if all(key in row and row[key] == value for key, value in filters.items()):
                deleted += 1
            else:
                remaining.append(row)

        self._tables[table] = remaining
        return deleted
