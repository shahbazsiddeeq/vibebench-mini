"""A small, thread-safe in-memory database."""

from __future__ import annotations

from threading import RLock
from typing import Any


class MemDB:
    """Store and query dictionary rows grouped by table name."""

    def __init__(self) -> None:
        self._tables: dict[str, list[dict[str, Any]]] = {}
        self._lock = RLock()

    @staticmethod
    def _validate_table(table: str) -> None:
        if not isinstance(table, str):
            raise TypeError("table must be a string")
        if not table:
            raise ValueError("table must not be empty")

    @staticmethod
    def _matches(row: dict[str, Any], filters: dict[str, Any]) -> bool:
        return all(key in row and row[key] == value for key, value in filters.items())

    def insert(self, table: str, row: dict[str, Any]) -> None:
        """Insert a row into a table."""
        self._validate_table(table)
        if not isinstance(row, dict):
            raise TypeError("row must be a dictionary")
        if not all(isinstance(key, str) for key in row):
            raise TypeError("row keys must be strings")

        with self._lock:
            self._tables.setdefault(table, []).append(row.copy())

    def find(self, table: str, **filters: Any) -> list[dict[str, Any]]:
        """Return rows matching all filters, or all rows if none are given."""
        self._validate_table(table)

        with self._lock:
            rows = self._tables.get(table, ())
            return [row.copy() for row in rows if self._matches(row, filters)]

    def delete(self, table: str, **filters: Any) -> int:
        """Delete rows matching all filters and return the number removed."""
        self._validate_table(table)

        with self._lock:
            rows = self._tables.get(table)
            if not rows:
                return 0

            retained = [row for row in rows if not self._matches(row, filters)]
            deleted = len(rows) - len(retained)

            if retained:
                self._tables[table] = retained
            else:
                self._tables.pop(table, None)

            return deleted
