"""Safe Sort Query Builder.

Provides fetch_sorted, a helper that builds a parameterized/whitelisted
SELECT ... ORDER BY query for sqlite3 connections while defending against
SQL injection via strict identifier validation and column whitelisting.
"""

import re
import sqlite3
from typing import Collection, Optional

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _validate_identifier(value: str, label: str) -> str:
    if not isinstance(value, str) or not _IDENTIFIER_RE.match(value):
        raise ValueError(f"Invalid {label} identifier")
    return value


def fetch_sorted(
    conn: sqlite3.Connection,
    table: str,
    sort_column: str,
    allowed_columns: Collection[str],
    descending: bool = False,
    limit: Optional[int] = None,
) -> list:
    """Run a safely constructed SELECT ... ORDER BY query and return rows.

    Security measures:
      - table and sort_column must match a strict identifier pattern and
        are double-quoted when embedded in SQL.
      - sort_column must be a member of allowed_columns (whitelist check).
      - descending is a bool, never a raw string, controlling ASC/DESC.
      - limit, if provided, must be a non-negative int and is passed as a
        bound parameter (?), never string-interpolated.
      - The caller's connection is never closed by this function.
    """
    if not isinstance(conn, sqlite3.Connection):
        raise ValueError("Invalid connection")

    if allowed_columns is None:
        raise ValueError("allowed_columns must be provided")

    # Validate identifiers first (defense in depth), then whitelist.
    safe_table = _validate_identifier(table, "table")
    safe_column = _validate_identifier(sort_column, "sort_column")

    if safe_column not in allowed_columns:
        raise ValueError("sort_column is not in allowed_columns")

    if not isinstance(descending, bool):
        raise ValueError("descending must be a bool")

    direction = "DESC" if descending else "ASC"

    params: list = []
    limit_clause = ""
    if limit is not None:
        if isinstance(limit, bool) or not isinstance(limit, int):
            raise ValueError("limit must be a non-negative int or None")
        if limit < 0:
            raise ValueError("limit must be a non-negative int or None")
        limit_clause = " LIMIT ?"
        params.append(limit)

    query = (
        f'SELECT * FROM "{safe_table}" '
        f'ORDER BY "{safe_column}" {direction}, rowid ASC'
        f"{limit_clause}"
    )

    try:
        cursor = conn.execute(query, params)
        rows = cursor.fetchall()
    except sqlite3.Error:
        # Do not leak internal DB error details.
        raise ValueError("Query execution failed")

    return [tuple(row) for row in rows]
