"""
src/solution.py

Secure SQLite batch insert utility.

Provides a single public function, ``batch_insert``, which inserts a list
of dict-rows into a specified table within a single transaction. On any
failure, the entire transaction is rolled back and a ``RuntimeError`` is
raised. Malformed identifiers (table/column names) are rejected early with
a ``ValueError`` before any database interaction takes place.
"""

import re
import sqlite3
from typing import Any, Dict, List

# Identifiers must start with a letter or underscore and contain only
# alphanumeric characters and underscores. This prevents SQL injection via
# table or column names, since these cannot be parameterized in SQLite.
_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _validate_identifier(name: Any, kind: str) -> str:
    """Validate a table or column name.

    Raises ValueError if the identifier is not a safe, simple identifier.
    """
    if not isinstance(name, str) or not _IDENTIFIER_RE.match(name):
        raise ValueError(f"Invalid {kind} name")
    return name


def _validate_rows_structure(rows: Any) -> List[Dict[str, Any]]:
    """Validate the basic structure of rows (non-column-name related).

    Ensures rows is a non-empty list of non-empty dicts with identical
    key sets. Raises ValueError on structural problems -- callers should
    catch this and re-raise as RuntimeError, except for column-name
    validity which is checked separately and must propagate as
    ValueError.
    """
    if not isinstance(rows, list) or len(rows) == 0:
        raise ValueError("rows must be a non-empty list of dicts")

    first_keys = None
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("each row must be a dict")
        if len(row) == 0:
            raise ValueError("rows must not be empty dicts")

        keys = set(row.keys())
        if first_keys is None:
            first_keys = keys
        elif keys != first_keys:
            raise ValueError("all rows must have the same set of columns")

    return rows


def batch_insert(db_path: str, table: str, rows: List[Dict[str, Any]]) -> int:
    """Insert all rows into table within a single transaction.

    Args:
        db_path: Path to the SQLite database file.
        table: Name of the table to insert into.
        rows: List of dicts mapping column name -> value. All rows must
              share the same set of keys.

    Returns:
        The number of rows inserted.

    Raises:
        ValueError: If the table name or any column name is not a valid,
            safe SQL identifier.
        RuntimeError: If the rows argument is malformed (e.g. mismatched
            keys, not a list of dicts) or if any database error occurs
            during the transaction. The transaction is rolled back in
            full on any failure.
    """
    # Validate the table name first; this must raise ValueError directly.
    _validate_identifier(table, "table")

    # Validate the general shape of `rows` (list of dicts, matching keys).
    # Structural problems here should surface as RuntimeError per the
    # contract, so we catch and re-raise.
    try:
        validated_rows = _validate_rows_structure(rows)
    except ValueError as exc:
        raise RuntimeError(f"Invalid rows argument: {exc}") from None

    # Validate column names; invalid identifiers must raise ValueError
    # directly (not wrapped), to guard against SQL injection attempts.
    columns = sorted(validated_rows[0].keys())
    for col in columns:
        _validate_identifier(col, "column")

    quoted_columns = ", ".join(f'"{c}"' for c in columns)
    placeholders = ", ".join(f":{c}" for c in columns)
    sql = f'INSERT INTO "{table}" ({quoted_columns}) VALUES ({placeholders})'

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("BEGIN")
        for row in validated_rows:
            conn.execute(sql, row)
        conn.commit()
        return len(validated_rows)
    except Exception as exc:
        if conn is not None:
            try:
                conn.rollback()
            except Exception:
                pass
        raise RuntimeError("Batch insert failed") from None
    finally:
        if conn is not None:
            conn.close()
