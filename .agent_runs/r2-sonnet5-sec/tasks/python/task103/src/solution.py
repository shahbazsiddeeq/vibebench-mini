"""
Secure Query Builder (fluent interface) that produces parameterized SQL.

Only the *values* bound via where()/limit() are treated as untrusted data and
are always passed back as separate parameters (using "?" placeholders) rather
than being interpolated into the SQL string. Because table and column names
cannot be parameterized in standard SQL, they are strictly validated against
a safe identifier whitelist to prevent SQL injection through those vectors.
"""

import re
from typing import Any, List, Tuple

# Identifiers: letters, digits, underscores; must not start with a digit.
_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

_MAX_IDENTIFIER_LENGTH = 128
_MAX_LIMIT = 10_000_000  # sane upper bound to avoid abuse


class QueryBuilderError(ValueError):
    """Raised when the query builder receives invalid input."""


def _validate_identifier(name: Any, kind: str) -> str:
    if not isinstance(name, str):
        raise QueryBuilderError(f"Invalid {kind}: must be a string")
    if len(name) == 0 or len(name) > _MAX_IDENTIFIER_LENGTH:
        raise QueryBuilderError(f"Invalid {kind}: length out of bounds")
    if not _IDENTIFIER_RE.match(name):
        raise QueryBuilderError(f"Invalid {kind}: contains illegal characters")
    return name


class QueryBuilder:
    """Fluent builder for parameterized SQL SELECT statements."""

    __slots__ = ("_table", "_columns", "_conditions", "_params", "_limit")

    def __init__(self, table: str) -> None:
        self._table = _validate_identifier(table, "table name")
        self._columns: List[str] = ["*"]
        self._conditions: List[str] = []
        self._params: List[Any] = []
        self._limit: int | None = None

    def select(self, *columns: str) -> "QueryBuilder":
        if not columns:
            raise QueryBuilderError("select() requires at least one column")
        validated = [_validate_identifier(c, "column name") for c in columns]
        self._columns = validated
        return self

    def where(self, column: str, value: Any) -> "QueryBuilder":
        col = _validate_identifier(column, "column name")
        self._conditions.append(f"{col} = ?")
        self._params.append(value)
        return self

    def limit(self, n: Any) -> "QueryBuilder":
        if isinstance(n, bool) or not isinstance(n, int):
            raise QueryBuilderError("limit() requires an integer")
        if n < 0 or n > _MAX_LIMIT:
            raise QueryBuilderError("limit() value out of allowed range")
        self._limit = n
        return self

    def build(self) -> Tuple[str, List[Any]]:
        columns_sql = ", ".join(self._columns)
        sql = f"SELECT {columns_sql} FROM {self._table}"
        params: List[Any] = list(self._params)

        if self._conditions:
            sql += " WHERE " + " AND ".join(self._conditions)

        if self._limit is not None:
            sql += " LIMIT ?"
            params.append(self._limit)

        return sql, params
