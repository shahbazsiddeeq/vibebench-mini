"""
In-memory database module.

Provides a simple, thread-safe-ish (single-process) in-memory table store
supporting insert, find (AND of filters), and delete operations.

Security considerations:
- All inputs are strictly validated (table names must be non-empty strings,
  rows must be dicts with string keys, filter keys must be strings).
- No use of eval/exec or dynamic code execution.
- Rows are deep-copied on insert/return to avoid accidental external
  mutation of internal state (defensive copying).
- Errors raised are generic (TypeError/ValueError) without leaking internal
  state or stack traces.
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List


class MemDB:
    """A minimal in-memory database supporting multiple named tables."""

    def __init__(self) -> None:
        # Internal storage: table name -> list of row dicts.
        self._tables: Dict[str, List[Dict[str, Any]]] = {}

    @staticmethod
    def _validate_table_name(table: str) -> None:
        if not isinstance(table, str) or not table:
            raise TypeError("table name must be a non-empty string")

    @staticmethod
    def _validate_row(row: Dict[str, Any]) -> None:
        if not isinstance(row, dict):
            raise TypeError("row must be a dict")
        for key in row.keys():
            if not isinstance(key, str):
                raise TypeError("row keys must be strings")

    @staticmethod
    def _validate_filters(filters: Dict[str, Any]) -> None:
        for key in filters.keys():
            if not isinstance(key, str):
                raise TypeError("filter keys must be strings")

    def insert(self, table: str, row: Dict[str, Any]) -> None:
        """Insert a row (dict) into the named table."""
        self._validate_table_name(table)
        self._validate_row(row)

        # Deep copy to prevent external mutation of stored data.
        stored_row = copy.deepcopy(row)

        if table not in self._tables:
            self._tables[table] = []
        self._tables[table].append(stored_row)

    def find(self, table: str, **filters: Any) -> List[Dict[str, Any]]:
        """Return list of rows matching all filters (AND). No filters -> all rows."""
        self._validate_table_name(table)
        self._validate_filters(filters)

        rows = self._tables.get(table, [])
        result = []
        for row in rows:
            if self._matches(row, filters):
                result.append(copy.deepcopy(row))
        return result

    def delete(self, table: str, **filters: Any) -> int:
        """Delete rows matching all filters (AND). Returns count of deleted rows."""
        self._validate_table_name(table)
        self._validate_filters(filters)

        if table not in self._tables:
            return 0

        original_rows = self._tables[table]
        remaining_rows = []
        deleted_count = 0

        for row in original_rows:
            if self._matches(row, filters):
                deleted_count += 1
            else:
                remaining_rows.append(row)

        self._tables[table] = remaining_rows
        return deleted_count

    @staticmethod
    def _matches(row: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        for key, value in filters.items():
            if key not in row or row[key] != value:
                return False
        return True
