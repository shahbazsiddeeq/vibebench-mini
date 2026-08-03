from __future__ import annotations

import re
import sqlite3


def value_counts(db_path: str, table: str, column: str) -> dict:
    if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", table):
        raise ValueError(f"invalid table name: {table}")
    if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", column):
        raise ValueError(f"invalid column name: {column}")
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            f"SELECT {column}, COUNT(*) FROM {table} GROUP BY {column}"
        ).fetchall()
    return {value: count for value, count in rows}
