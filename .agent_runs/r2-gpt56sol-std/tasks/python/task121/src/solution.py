import operator
import re
import sqlite3
from os import PathLike
from typing import Any


_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")


def paginate(
    db_path: str | bytes | PathLike[str] | PathLike[bytes],
    table: str,
    page: int,
    page_size: int,
) -> list[tuple[Any, ...]]:
    """Return a 1-based page of table rows ordered by SQLite rowid."""
    if not isinstance(table, str) or _IDENTIFIER.fullmatch(table) is None:
        raise ValueError("invalid table name")

    try:
        page = operator.index(page)
        page_size = operator.index(page_size)
    except TypeError as exc:
        raise ValueError("page and page_size must be positive integers") from exc

    if page < 1 or page_size < 1:
        raise ValueError("page and page_size must be at least 1")

    offset = (page - 1) * page_size
    query = f'SELECT * FROM "{table}" ORDER BY rowid LIMIT ? OFFSET ?'

    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.execute(query, (page_size, offset))
        return [tuple(row) for row in cursor.fetchall()]
    finally:
        connection.close()
