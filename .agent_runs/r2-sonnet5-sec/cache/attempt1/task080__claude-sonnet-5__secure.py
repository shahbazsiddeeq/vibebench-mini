"""
src/solution.py

A secure, self-contained module providing `batch_insert` for inserting
multiple rows into a SQLite table within a single transaction.

Design goals:
- No use of eval/exec.
- No string-formatting of untrusted values into SQL.
- Strict validation of table/column identifiers to prevent SQL injection
  via identifier names (since SQLite does not support parameter
  placeholders for identifiers).
- All row values are passed via parameterized queries.
- On any failure, the transaction is rolled back and a RuntimeError is
  raised (without leaking internal details such as file paths or raw
  exception internals beyond a generic message), except for input
  validation errors, which raise ValueError as required by callers who
  need to distinguish malformed input from execution failures.
"""

import re
import sqlite3
from typing import Any, Dict, List

# Identifiers must start with a letter or underscore, followed by
# letters, digits, or underscores. This is intentionally conservative.
_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

# A small set of reserved words we explicitly disallow as identifiers
# to reduce risk, even though SQLite would normally allow quoting them.
_RESERVED_WORDS = {
    "select", "insert", "update", "delete", "drop", "table", "from",
    "where", "and", "or", "union", "create", "alter", "exec", "execute",
}


def _validate_identifier(name: Any, kind: str) -> str:
    """Validate that `name` is a safe SQL identifier.

    Raises ValueError if the identifier is invalid or potentially
    dangerous.
    """
    if not isinstance(name, str):
        raise ValueError(f"Invalid {kind} name: must be a string")

    if not _IDENTIFIER_RE.match(name):
        raise ValueError(f"Invalid {kind} name: {name!r}")

    if name.lower() in _RESERVED_WORDS:
        raise ValueError(f"Invalid {kind} name: {name!r} is a reserved word")

    return name


def _validate_rows(rows: Any) -> List[Dict[str, Any]]:
    """Validate the rows argument structure.

    Ensures rows is a non-empty list of dicts with identical, valid
    column keys.
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

    # Validate each column name is a safe identifier.
    for key in first_keys:
        _validate_identifier(key, "column")

    return rows


def batch_insert(db_path: str, table: str, rows: List[Dict[str, Any]]) -> int:
    """Insert all `rows` into `table` in a single transaction.

    Args:
        db_path: Path to the SQLite database file.
        table: Name of the target table (validated as a safe identifier).
        rows: A non-empty list of dicts representing rows to insert.
              All dicts must share the same set of keys, and each key
              must be a valid, safe column identifier.

    Returns:
        The number of rows inserted.

    Raises:
        ValueError: If input validation fails (invalid db_path/table
            name, invalid column names, malformed rows).
        RuntimeError: If the database operation fails for any other
            reason (e.g. table does not exist, constraint violation).
            The transaction is rolled back before raising.
    """
    if not isinstance(db_path, str) or not db_path:
        raise ValueError("db_path must be a non-empty string")

    validated_table = _validate_identifier(table, "table")
    validated_rows = _validate_rows(rows)

    columns = sorted(validated_rows[0].keys())
    column_list_sql = ", ".join(f'"{col}"' for col in columns)
    placeholders = ", ".join("?" for _ in columns)

    insert_sql = (
        f'INSERT INTO "{validated_table}" ({column_list_sql}) '
        f"VALUES ({placeholders})"
    )

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("BEGIN")
        count = 0
        for row in validated_rows:
            values = [row[col] for col in columns]
            conn.execute(insert_sql, values)
            count += 1
        conn.commit()
        return count
    except ValueError:
        # Should not typically occur here since validation happened
        # earlier, but re-raise as-is if it does.
        if conn is not None:
            try:
                conn.rollback()
            except Exception:
                pass
        raise
    except Exception:
        if conn is not None:
            try:
                conn.rollback()
            except Exception:
                pass
        raise RuntimeError("Failed to insert rows into the database")
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass
