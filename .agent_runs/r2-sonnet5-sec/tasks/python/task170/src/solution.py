"""
src/solution.py

Secure parameterized row filter for SQLite tables.

Provides select_where(conn, table, filters) which builds a SQL query using
only validated identifiers (table name and filter keys) and safely bound
parameters for all values, preventing SQL injection.
"""

import re
import sqlite3
from typing import Any, Dict, List, Tuple

# Identifiers (table names, column names) must match this pattern.
_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _validate_identifier(name: str) -> str:
    """
    Validate that `name` is a safe SQL identifier.

    Raises ValueError if the identifier does not match the required pattern.
    Returns the identifier wrapped in double quotes for safe embedding in SQL.
    """
    if not isinstance(name, str) or not _IDENTIFIER_RE.match(name):
        raise ValueError("Invalid identifier: identifiers must match ^[A-Za-z_][A-Za-z0-9_]*$")
    # Escape any embedded double quotes just in case (defense in depth),
    # though the regex already disallows them.
    escaped = name.replace('"', '""')
    return f'"{escaped}"'


def select_where(
    conn: sqlite3.Connection,
    table: str,
    filters: Dict[str, Any],
) -> List[Tuple[Any, ...]]:
    """
    Run a parameterized SELECT * FROM <table> query filtering rows where
    every key in `filters` equals its corresponding value, combined with AND.

    Args:
        conn: An open sqlite3.Connection. This function does NOT close it.
        table: The table name (must match ^[A-Za-z_][A-Za-z0-9_]*$).
        filters: A dict mapping column name -> value. Column names must
            match the same identifier pattern. A value of None matches
            rows where the column IS NULL.

    Returns:
        A list of tuples representing the matching rows, in the table's
        column definition order, ordered by rowid ascending.

    Raises:
        ValueError: If the table name or any filter key is not a valid
            identifier, or if `filters` is not a dict.
    """
    if not isinstance(conn, sqlite3.Connection):
        raise ValueError("conn must be a sqlite3.Connection instance")

    if not isinstance(filters, dict):
        raise ValueError("filters must be a dict")

    # Validate and quote the table identifier.
    quoted_table = _validate_identifier(table)

    where_clauses: List[str] = []
    params: List[Any] = []

    for key, value in filters.items():
        quoted_col = _validate_identifier(key)
        if value is None:
            where_clauses.append(f"{quoted_col} IS NULL")
        else:
            where_clauses.append(f"{quoted_col} = ?")
            params.append(value)

    sql = f"SELECT * FROM {quoted_table}"
    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)
    sql += " ORDER BY rowid ASC"

    try:
        cursor = conn.execute(sql, params)
        rows = cursor.fetchall()
    except sqlite3.Error as exc:
        # Do not leak internal details; raise a generic error.
        raise ValueError("Failed to execute query against the database") from exc

    return [tuple(row) for row in rows]
