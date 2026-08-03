import re
import sqlite3
from typing import Any


_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _quote_identifier(identifier: Any) -> str:
    if not isinstance(identifier, str) or _IDENTIFIER_RE.fullmatch(identifier) is None:
        raise ValueError(f"Invalid SQL identifier: {identifier!r}")
    return f'"{identifier}"'


def bulk_update(
    conn: sqlite3.Connection,
    table: str,
    key_column: str,
    rows: list[dict],
) -> int:
    """Update multiple rows atomically and return the total affected row count."""
    if not isinstance(rows, list):
        raise ValueError("rows must be a list")

    quoted_table = _quote_identifier(table)
    quoted_key = _quote_identifier(key_column)

    if not rows:
        return 0

    statements: list[tuple[str, tuple[Any, ...]]] = []

    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("each row must be a dict")
        if key_column not in row:
            raise ValueError(f"row is missing key column {key_column!r}")

        set_columns = [column for column in row if column != key_column]
        if not set_columns:
            raise ValueError("each row must contain at least one column to update")

        quoted_set_columns = [_quote_identifier(column) for column in set_columns]
        assignments = ", ".join(
            f"{column}=?" for column in quoted_set_columns
        )
        sql = (
            f"UPDATE {quoted_table} SET {assignments} "
            f"WHERE {quoted_key}=?"
        )
        parameters = tuple(row[column] for column in set_columns) + (
            row[key_column],
        )
        statements.append((sql, parameters))

    savepoint = '"bulk_update_savepoint"'
    conn.execute(f"SAVEPOINT {savepoint}")

    try:
        total = 0
        for sql, parameters in statements:
            cursor = conn.execute(sql, parameters)
            total += cursor.rowcount

        conn.execute(f"RELEASE SAVEPOINT {savepoint}")
        return int(total)
    except BaseException:
        try:
            conn.execute(f"ROLLBACK TO SAVEPOINT {savepoint}")
        except Exception:
            pass
        try:
            conn.execute(f"RELEASE SAVEPOINT {savepoint}")
        except Exception:
            pass
        raise
