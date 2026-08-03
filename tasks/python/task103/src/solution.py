"""Builder pattern: a fluent, parameterized SQL SELECT query builder."""
from __future__ import annotations

from typing import Any


class QueryBuilder:
    def __init__(self, table: str):
        self._table = table
        self._columns: list[str] = ["*"]
        self._conditions: list[str] = []
        self._params: list[Any] = []
        self._limit: int | None = None

    def select(self, *columns: str) -> "QueryBuilder":
        self._columns = list(columns) if columns else ["*"]
        return self

    def where(self, column: str, value: Any) -> "QueryBuilder":
        self._conditions.append(f"{column} = ?")
        self._params.append(value)
        return self

    def limit(self, n: int) -> "QueryBuilder":
        self._limit = n
        return self

    def build(self) -> tuple[str, list]:
        cols = ", ".join(self._columns)
        sql = f"SELECT {cols} FROM {self._table}"
        params = list(self._params)
        if self._conditions:
            sql += " WHERE " + " AND ".join(self._conditions)
        if self._limit is not None:
            sql += " LIMIT ?"
            params.append(self._limit)
        return sql, params
