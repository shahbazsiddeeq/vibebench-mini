from __future__ import annotations

import re
import sqlite3

_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
# Column types may carry constraints (e.g. "INTEGER PRIMARY KEY", "VARCHAR(255)").
# Restrict to a safe alphabet that cannot break out of the DDL.
_TYPE = re.compile(r"^[A-Za-z0-9_ ()]+$")


def _quote_ident(name: str) -> str:
    if not _IDENT.match(name):
        raise ValueError(f"invalid identifier: {name}")
    return '"' + name + '"'


def create_table(db_path: str, table_name: str, columns: dict[str, str]) -> None:
    quoted_table = _quote_ident(table_name)
    if not columns:
        raise ValueError("columns must not be empty")
    col_defs = []
    for name, dtype in columns.items():
        quoted_col = _quote_ident(name)
        if not _TYPE.match(dtype):
            raise ValueError(f"invalid column type: {dtype}")
        col_defs.append(f"{quoted_col} {dtype}")
    col_sql = ", ".join(col_defs)

    conn = sqlite3.connect(db_path)
    try:
        existing = {
            r[0].lower()
            for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
        if table_name.lower() in existing:
            raise ValueError(f"table '{table_name}' already exists")
        conn.execute(f"CREATE TABLE {quoted_table} ({col_sql})")
        conn.commit()
    finally:
        conn.close()
