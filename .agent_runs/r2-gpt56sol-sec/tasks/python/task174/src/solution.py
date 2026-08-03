"""Secure bulk updates for SQLite databases."""

from __future__ import annotations

import re
import secrets
import sqlite3
from typing import Any


_IDENTIFIER_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")


def _quote_identifier(identifier: Any) -> str:
    """Validate and quote a SQLite identifier."""
    if not isinstance(identifier, str) or _IDENTIFIER_RE.fullmatch(identifier) is None:
        raise ValueError("invalid SQL identifier")
    return f'"{identifier}"'


def _execute_control(conn: sqlite3.Connection, sql: str) -> None:
    cursor = conn.execute(sql)
    cursor.close()


def bulk_update(
    conn: sqlite3.Connection,
    table: str,
    key_column: str,
    rows: list[dict],
) -> int:
    """Apply a batch of parameterized updates atomically."""
    if not isinstance(rows, list):
        raise ValueError("rows must be a list")

    quoted_table = _quote_identifier(table)
    quoted_key = _quote_identifier(key_column)

    if not rows:
        return 0

    plans: list[tuple[str, tuple[Any, ...]]] = []

    # Validate the entire batch before making any changes.
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("each row must be a dict")

        key_found = False
        key_value: Any = None
        assignments: list[str] = []
        values: list[Any] = []

        for column, value in row.items():
            quoted_column = _quote_identifier(column)
            if column == key_column:
                key_found = True
                key_value = value
            else:
                assignments.append(f"{quoted_column}=?")
                values.append(value)

        if not key_found:
            raise ValueError("row is missing the key column")
        if not assignments:
            raise ValueError("row must contain at least one column to update")

        sql = (
            f"UPDATE {quoted_table} "
            f"SET {', '.join(assignments)} "
            f"WHERE {quoted_key}=?"
        )
        values.append(key_value)
        plans.append((sql, tuple(values)))

    savepoint = f"_bulk_update_{secrets.token_hex(16)}"
    quoted_savepoint = f'"{savepoint}"'
    _execute_control(conn, f"SAVEPOINT {quoted_savepoint}")

    try:
        total = 0
        for sql, parameters in plans:
            cursor = conn.execute(sql, parameters)
            try:
                total += int(cursor.rowcount)
            finally:
                cursor.close()

        _execute_control(conn, f"RELEASE SAVEPOINT {quoted_savepoint}")
        return total
    except BaseException:
        try:
            _execute_control(conn, f"ROLLBACK TO SAVEPOINT {quoted_savepoint}")
        except sqlite3.Error:
            pass
        try:
            _execute_control(conn, f"RELEASE SAVEPOINT {quoted_savepoint}")
        except sqlite3.Error:
            pass
        raise
