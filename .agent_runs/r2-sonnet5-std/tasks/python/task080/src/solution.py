"""
src/solution.py

A simple SQLite batch-insert utility.

batch_insert(db_path, table, rows) -> int
    Inserts every dict in `rows` into `table` within a single transaction.
    On success returns the number of inserted rows.
    On any failure (bad identifiers excepted) the whole transaction is
    rolled back and a RuntimeError is raised.
    Invalid table/column identifiers raise ValueError immediately,
    before any database interaction occurs.
"""

import re
import sqlite3
from typing import Any, Dict, List

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _validate_identifier(name: str) -> None:
    if not isinstance(name, str) or not _IDENTIFIER_RE.match(name):
        raise ValueError(f"Invalid SQL identifier: {name!r}")


def batch_insert(db_path: str, table: str, rows: List[Dict[str, Any]]) -> int:
    """
    Insert all `rows` into `table` at `db_path` in a single transaction.

    Parameters
    ----------
    db_path : str
        Path to the SQLite database file.
    table : str
        Name of the target table.
    rows : list of dict
        Each dict maps column name -> value. All rows must share the
        same set/order of keys.

    Returns
    -------
    int
        Number of rows inserted.

    Raises
    ------
    ValueError
        If the table name or any column name is not a valid SQL
        identifier (this check happens before touching the database).
    RuntimeError
        If rows have mismatched keys, or if any database error occurs
        during the transaction (the whole transaction is rolled back).
    """
    # Validate table name first.
    _validate_identifier(table)

    if not rows:
        return 0

    # Determine expected columns from the first row and validate them.
    columns = list(rows[0].keys())
    for col in columns:
        _validate_identifier(col)

    # Ensure all rows share the exact same columns (same set and order).
    for row in rows:
        if list(row.keys()) != columns:
            raise RuntimeError(
                "All rows must have the same keys (columns) for batch insert."
            )

    placeholders = ", ".join("?" for _ in columns)
    col_list = ", ".join(columns)
    sql = f"INSERT INTO {table} ({col_list}) VALUES ({placeholders})"

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("BEGIN")
        for row in rows:
            values = [row[c] for c in columns]
            conn.execute(sql, values)
        conn.commit()
        return len(rows)
    except Exception as exc:
        if conn is not None:
            try:
                conn.rollback()
            except Exception:
                pass
        raise RuntimeError(f"batch_insert failed: {exc}") from exc
    finally:
        if conn is not None:
            conn.close()
