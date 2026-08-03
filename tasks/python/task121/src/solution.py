from __future__ import annotations

import re
import sqlite3


def paginate(db_path: str, table: str, page: int, page_size: int) -> list[tuple]:
    if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", table):
        raise ValueError(f"invalid table name: {table}")
    if page < 1:
        raise ValueError(f"page must be >= 1, got {page}")
    if page_size < 1:
        raise ValueError(f"page_size must be >= 1, got {page_size}")
    offset = (page - 1) * page_size
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            f"SELECT * FROM {table} ORDER BY rowid LIMIT ? OFFSET ?",
            (page_size, offset),
        ).fetchall()
    return rows
