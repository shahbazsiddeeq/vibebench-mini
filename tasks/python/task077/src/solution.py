from __future__ import annotations

import csv
import re
import sqlite3
from pathlib import Path

_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _quote_ident(name: str) -> str:
    if not _IDENT.match(name):
        raise ValueError(f"invalid identifier: {name}")
    return '"' + name + '"'


def csv_to_sqlite(csv_path: str, db_path: str, table_name: str) -> int:
    if not Path(csv_path).exists():
        raise FileNotFoundError(f"No such file: {csv_path}")

    quoted_table = _quote_ident(table_name)

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    if not fieldnames:
        return 0

    quoted_cols = [_quote_ident(c) for c in fieldnames]
    col_sql = ", ".join(f"{qc} TEXT" for qc in quoted_cols)

    conn = sqlite3.connect(db_path)
    try:
        existing = {
            r[0]
            for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
        if table_name in existing:
            raise ValueError(f"table '{table_name}' already exists")
        conn.execute(f"CREATE TABLE {quoted_table} ({col_sql})")
        placeholders = ", ".join("?" for _ in fieldnames)
        conn.executemany(
            f"INSERT INTO {quoted_table} VALUES ({placeholders})",
            [[row[c] for c in fieldnames] for row in rows],
        )
        conn.commit()
    finally:
        conn.close()
    return len(rows)
