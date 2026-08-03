"""
src/solution.py

Provides a safe SQLite upsert helper.

upsert(db_path, table, record, key) inserts `record` into `table`, or on a
conflict of the unique/primary-key column `key`, updates the existing row:
every column present in `record` (other than `key`) is overwritten with the
new value; columns absent from `record` are left unchanged.

Security notes:
  * `table`, `key`, and every key in `record` must match the identifier
    pattern [A-Za-z_][A-Za-z0-9_]*; anything else raises ValueError.
  * Identifiers are double-quoted when interpolated into SQL.
  * All values are passed as bound parameters, never interpolated directly.
  * Raises KeyError if `key` is not a key of `record`.
"""

import re
import sqlite3
from typing import Any, Dict

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _validate_identifier(name: Any) -> str:
    """Validate that `name` is a safe SQL identifier, return it as a string.

    Raises ValueError if `name` is not a string matching the required
    pattern.
    """
    if not isinstance(name, str) or not _IDENTIFIER_RE.match(name):
        raise ValueError(f"Invalid identifier: {name!r}")
    return name


def _quote_identifier(name: str) -> str:
    """Double-quote an already-validated identifier for safe interpolation."""
    return '"' + name.replace('"', '""') + '"'


def upsert(db_path: str, table: str, record: Dict[str, Any], key: str) -> None:
    """
    Insert `record` into `table`, or update on conflict of `key`.

    :param db_path: path to the SQLite database file.
    :param table: table name (validated identifier).
    :param record: mapping of column name -> value; must contain `key`.
    :param key: the column name that has a UNIQUE/PRIMARY KEY constraint.
    :raises ValueError: if table, key, or any record column name is not a
        valid identifier.
    :raises KeyError: if `key` is not present in `record`.
    """
    if not isinstance(record, dict):
        raise ValueError("record must be a dict")

    # Validate table and key identifiers first.
    table = _validate_identifier(table)
    key = _validate_identifier(key)

    if key not in record:
        raise KeyError(key)

    # Validate all column names in record.
    validated_columns = []
    for col in record.keys():
        validated_columns.append(_validate_identifier(col))

    quoted_table = _quote_identifier(table)
    quoted_key = _quote_identifier(key)

    columns = list(record.keys())
    quoted_columns = [_quote_identifier(c) for c in columns]
    values = [record[c] for c in columns]

    placeholders = ", ".join("?" for _ in columns)
    columns_sql = ", ".join(quoted_columns)

    update_columns = [c for c in columns if c != key]

    insert_sql = (
        f"INSERT INTO {quoted_table} ({columns_sql}) VALUES ({placeholders})"
    )

    if update_columns:
        set_clause = ", ".join(
            f"{_quote_identifier(c)} = excluded.{_quote_identifier(c)}"
            for c in update_columns
        )
        insert_sql += f" ON CONFLICT({quoted_key}) DO UPDATE SET {set_clause}"
    else:
        # Only the key column was provided; leave existing row untouched.
        insert_sql += f" ON CONFLICT({quoted_key}) DO NOTHING"

    conn = sqlite3.connect(db_path)
    try:
        with conn:
            conn.execute(insert_sql, values)
    finally:
        conn.close()
