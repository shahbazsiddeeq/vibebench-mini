"""Secure parameterized SQLite row filtering."""

from __future__ import annotations

import re
import sqlite3
from typing import Any


_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _quote_identifier(identifier: object) -> str:
    """Validate and quote a SQLite identifier."""
    if not isinstance(identifier, str) or _IDENTIFIER_RE.fullmatch(identifier) is None:
        raise ValueError("invalid SQL identifier")
    return f'"{identifier}"'


def select_where(
    conn: sqlite3.Connection,
    table: str,
    filters: dict,
) -> list[tuple]:
    """Return rows from *table* matching all filters, ordered by rowid."""
    if not isinstance(conn, sqlite3.Connection):
        raise TypeError("conn must be a sqlite3.Connection")
    if not isinstance(filters, dict):
        raise TypeError("filters must be a dict")

    quoted_table = _quote_identifier(table)
    conditions: list[str] = []
    parameters: list[Any] = []

    for column, value in filters.items():
        quoted_column = _quote_identifier(column)
        if value is None:
            conditions.append(f"{quoted_column} IS NULL")
        else:
            conditions.append(f"{quoted_column} = ?")
            parameters.append(value)

    sql = f"SELECT * FROM {quoted_table}"
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    sql += " ORDER BY rowid ASC"

    cursor = conn.execute(sql, parameters)
    try:
        return [tuple(row) for row in cursor.fetchall()]
    finally:
        cursor.close()
