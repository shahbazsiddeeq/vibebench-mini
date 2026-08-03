"""Safely build and execute a sorted SQLite query."""

from __future__ import annotations

import re
import sqlite3
from collections.abc import Collection

_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def fetch_sorted(
    conn: sqlite3.Connection,
    table: str,
    sort_column: str,
    allowed_columns: Collection[str],
    descending: bool = False,
    limit: int | None = None,
) -> list[tuple]:
    """Return table rows ordered by an approved column and then by rowid."""
    if not isinstance(conn, sqlite3.Connection):
        raise ValueError("conn must be a sqlite3.Connection")

    if not isinstance(table, str) or _IDENTIFIER_PATTERN.fullmatch(table) is None:
        raise ValueError("invalid table identifier")

    if not isinstance(sort_column, str):
        raise ValueError("invalid sort column")

    try:
        is_allowed = sort_column in allowed_columns
    except (TypeError, AttributeError):
        raise ValueError("allowed_columns must support membership checks") from None

    if not is_allowed:
        raise ValueError("sort column is not allowed")

    if _IDENTIFIER_PATTERN.fullmatch(sort_column) is None:
        raise ValueError("invalid sort column identifier")

    if not isinstance(descending, bool):
        raise ValueError("descending must be a bool")

    if limit is not None and (type(limit) is not int or limit < 0):
        raise ValueError("limit must be a non-negative int or None")

    direction = "DESC" if descending else "ASC"
    sql = (
        f'SELECT * FROM "{table}" '
        f'ORDER BY "{sort_column}" {direction}, rowid ASC'
    )
    parameters: tuple[int, ...] = ()

    if limit is not None:
        sql += " LIMIT ?"
        parameters = (limit,)

    cursor = conn.cursor()
    try:
        cursor.row_factory = None
        cursor.execute(sql, parameters)
        return [tuple(row) for row in cursor.fetchall()]
    finally:
        cursor.close()
