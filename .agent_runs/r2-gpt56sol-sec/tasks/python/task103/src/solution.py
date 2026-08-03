"""Secure fluent builder for parameterized SQL SELECT statements."""

from __future__ import annotations

import re
from typing import Any


_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _validate_identifier(identifier: str, *, allow_wildcard: bool = False) -> str:
    """Validate a possibly qualified SQL identifier."""
    if not isinstance(identifier, str):
        raise TypeError("SQL identifiers must be strings")
    if not identifier:
        raise ValueError("SQL identifiers cannot be empty")

    parts = identifier.split(".")
    for index, part in enumerate(parts):
        if allow_wildcard and part == "*" and index == len(parts) - 1:
            continue
        if not _IDENTIFIER.fullmatch(part):
            raise ValueError("Invalid SQL identifier")

    return identifier


class QueryBuilder:
    """Build a parameterized SQL SELECT statement using a fluent interface."""

    def __init__(self, table: str) -> None:
        self._table = _validate_identifier(table)
        self._columns: tuple[str, ...] = ("*",)
        self._conditions: list[tuple[str, Any]] = []
        self._limit: int | None = None

    def select(self, *columns: str) -> QueryBuilder:
        """Set the columns to select, defaulting to all columns."""
        if not columns:
            self._columns = ("*",)
        else:
            self._columns = tuple(
                _validate_identifier(column, allow_wildcard=True)
                for column in columns
            )
        return self

    def where(self, column: str, value: Any) -> QueryBuilder:
        """Add an equality condition with a bound parameter."""
        validated_column = _validate_identifier(column)
        self._conditions.append((validated_column, value))
        return self

    def limit(self, n: int) -> QueryBuilder:
        """Set a non-negative row limit as a bound parameter."""
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError("Limit must be an integer")
        if n < 0:
            raise ValueError("Limit cannot be negative")
        self._limit = n
        return self

    def build(self) -> tuple[str, list[Any]]:
        """Return the SQL statement and an independent ordered parameter list."""
        sql = f"SELECT {', '.join(self._columns)} FROM {self._table}"
        params: list[Any] = []

        if self._conditions:
            predicates = []
            for column, value in self._conditions:
                predicates.append(f"{column} = ?")
                params.append(value)
            sql += " WHERE " + " AND ".join(predicates)

        if self._limit is not None:
            sql += " LIMIT ?"
            params.append(self._limit)

        return sql, params
