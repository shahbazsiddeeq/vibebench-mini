"""SQLite row pagination utilities."""

from __future__ import annotations

import os
import re
import sqlite3
from contextlib import closing
from typing import Union

__all__ = ["paginate"]

_IDENTIFIER_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")
_SQLITE_MAX_INTEGER = 9_223_372_036_854_775_807

PathType = Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]


def paginate(
    db_path: PathType,
    table: str,
    page: int,
    page_size: int,
) -> list[tuple]:
    """Return a 1-based page of table rows ordered by SQLite rowid."""
    if not isinstance(table, str) or _IDENTIFIER_PATTERN.fullmatch(table) is None:
        raise ValueError("invalid table name")

    if isinstance(page, bool) or not isinstance(page, int) or page < 1:
        raise ValueError("page must be a positive integer")

    if isinstance(page_size, bool) or not isinstance(page_size, int) or page_size < 1:
        raise ValueError("page_size must be a positive integer")

    try:
        path = os.fspath(db_path)
    except TypeError as exc:
        raise ValueError("invalid database path") from exc

    if not isinstance(path, (str, bytes)):
        raise ValueError("invalid database path")

    offset = (page - 1) * page_size
    if offset > _SQLITE_MAX_INTEGER:
        return []

    # The physical limits of SQLite databases are below this row count, so an
    # unbounded LIMIT is equivalent when page_size exceeds SQLite's integer max.
    limit = page_size if page_size <= _SQLITE_MAX_INTEGER else -1
    quoted_table = f'"{table}"'
    query = (
        f"SELECT * FROM {quoted_table} "
        "ORDER BY rowid LIMIT ? OFFSET ?"
    )

    with closing(sqlite3.connect(path)) as connection:
        cursor = connection.execute(query, (limit, offset))
        return [tuple(row) for row in cursor.fetchall()]
