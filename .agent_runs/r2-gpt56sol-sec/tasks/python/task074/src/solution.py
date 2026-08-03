"""SQLite upsert utility."""

from __future__ import annotations

import os
import re
import sqlite3
from collections.abc import Mapping
from typing import Any


_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z", re.ASCII)


def _quote_identifier(value: object) -> str:
    """Validate and safely quote a SQLite identifier."""
    if not isinstance(value, str) or _IDENTIFIER.fullmatch(value) is None:
        raise ValueError(f"Invalid SQL identifier: {value!r}")
    return f'"{value}"'


def upsert(
    db_path: str | bytes | os.PathLike[str] | os.PathLike[bytes],
    table: str,
    record: Mapping[str, Any],
    key: str,
) -> None:
    """Insert a record or update its supplied non-key columns on conflict."""
    quoted_table = _quote_identifier(table)
    quoted_key = _quote_identifier(key)

    if not isinstance(record, Mapping):
        raise TypeError("record must be a mapping")

    items = list(record.items())
    for column, _ in items:
        _quote_identifier(column)

    if key not in record:
        raise KeyError(key)

    if not isinstance(db_path, (str, bytes, os.PathLike)):
        raise TypeError("db_path must be a path-like value")

    path = os.fspath(db_path)
    if "\x00" in path if isinstance(path, str) else b"\x00" in path:
        raise ValueError("db_path must not contain null bytes")

    columns = [column for column, _ in items]
    values = [value for _, value in items]
    quoted_columns = [_quote_identifier(column) for column in columns]

    placeholders = ", ".join("?" for _ in columns)
    sql = (
        f"INSERT INTO {quoted_table} ({', '.join(quoted_columns)}) "
        f"VALUES ({placeholders}) "
        f"ON CONFLICT ({quoted_key}) "
    )

    update_columns = [
        quoted_column
        for column, quoted_column in zip(columns, quoted_columns)
        if column != key
    ]
    if update_columns:
        assignments = ", ".join(
            f"{column}=excluded.{column}" for column in update_columns
        )
        sql += f"DO UPDATE SET {assignments}"
    else:
        sql += "DO NOTHING"

    with sqlite3.connect(path) as connection:
        connection.execute(sql, values)
