"""
Bulk Row Updater
================

Provides `bulk_update`, a helper that applies a batch of per-row UPDATE
statements to a SQLite table inside a single transaction, safely.

Security notes:
- All identifiers (table name, key column, set columns) are strictly
  validated against a safe pattern before being interpolated into SQL,
  and are double-quoted. No untrusted string is ever used to build the
  SQL text if it doesn't pass validation.
- All values (never identifiers) are passed as bound parameters via
  the DB-API `?` placeholders -- never string-formatted into SQL.
- The whole batch runs in a single transaction; any failure rolls back
  all changes so partial updates never persist.
- The caller-provided connection is never closed by this function.
"""

from __future__ import annotations

import re
import sqlite3
from typing import Any

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _validate_identifier(name: Any) -> str:
    """Validate that `name` is a safe SQL identifier and return it quoted.

    Raises ValueError if the identifier is invalid.
    """
    if not isinstance(name, str) or not _IDENTIFIER_RE.match(name):
        raise ValueError("Invalid identifier")
    return '"' + name + '"'


def bulk_update(
    conn: sqlite3.Connection,
    table: str,
    key_column: str,
    rows: list,
) -> int:
    """Apply per-row UPDATE statements to `table` inside a single transaction.

    For each dict in `rows`, builds:
        UPDATE <table> SET <col>=?, ... WHERE <key_column>=?
    where the SET columns/values come from the dict's entries other than
    key_column, and the WHERE value is the dict's key_column value.

    All identifiers (table, key_column, set columns) are validated against
    ^[A-Za-z_][A-Za-z0-9_]*$ and double-quoted; invalid identifiers raise
    ValueError. All values are bound as parameters.

    Returns the sum of each statement's cursor.rowcount.

    Raises ValueError for invalid input shapes/identifiers. If any statement
    fails during execution, the whole batch is rolled back.
    """
    if not isinstance(rows, list):
        raise ValueError("rows must be a list")

    if len(rows) == 0:
        return 0

    # Validate table and key column identifiers up front.
    quoted_table = _validate_identifier(table)
    quoted_key_column = _validate_identifier(key_column)

    # Pre-validate the key_column name string itself is usable as a dict key
    # lookup (it's just a string; already validated above for SQL safety).

    # Build the list of (sql, params) to execute, validating everything
    # before touching the database.
    statements = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("each row must be a dict")

        if key_column not in row:
            raise ValueError(f"row missing key column '{key_column}'")

        set_items = [(col, val) for col, val in row.items() if col != key_column]
        if not set_items:
            raise ValueError("row must contain at least one column to set")

        set_clauses = []
        params: list[Any] = []
        for col, val in set_items:
            quoted_col = _validate_identifier(col)
            set_clauses.append(f"{quoted_col}=?")
            params.append(val)

        key_value = row[key_column]
        params.append(key_value)

        sql = (
            f"UPDATE {quoted_table} SET {', '.join(set_clauses)} "
            f"WHERE {quoted_key_column}=?"
        )
        statements.append((sql, params))

    total_modified = 0
    try:
        conn.execute("BEGIN")
        cur = conn.cursor()
        for sql, params in statements:
            cur.execute(sql, params)
            rc = cur.rowcount
            if isinstance(rc, int) and rc > 0:
                total_modified += rc
        conn.commit()
    except Exception:
        conn.rollback()
        raise

    return total_modified
