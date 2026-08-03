"""SQLite column value counting utilities."""

from __future__ import annotations

import os
import re
import sqlite3
from typing import Any

_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z", re.ASCII)


def _validate_identifier(identifier: object, label: str) -> str:
    if not isinstance(identifier, str) or _IDENTIFIER.fullmatch(identifier) is None:
        raise ValueError(f"{label} must be a valid SQL identifier")
    return identifier


def value_counts(
    db_path: str | bytes | os.PathLike[str] | os.PathLike[bytes],
    table: str,
    column: str,
) -> dict[Any, int]:
    """Return a mapping of each distinct column value to its row count."""
    table_name = _validate_identifier(table, "table")
    column_name = _validate_identifier(column, "column")

    try:
        path = os.fspath(db_path)
    except TypeError as exc:
        raise TypeError("db_path must be a string, bytes, or path-like object") from exc

    if not isinstance(path, (str, bytes)) or not path:
        raise ValueError("db_path must not be empty")
    if "\x00" in path if isinstance(path, str) else b"\x00" in path:
        raise ValueError("db_path must not contain null bytes")

    query = (
        f'SELECT "{column_name}", COUNT(*) '
        f'FROM "{table_name}" '
        f'GROUP BY "{column_name}"'
    )

    with sqlite3.connect(path) as connection:
        rows = connection.execute(query).fetchall()

    return {value: int(count) for value, count in rows}
