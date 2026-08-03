from __future__ import annotations

import re
import sqlite3

_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _quote_ident(name: str) -> str:
    if not _IDENT.match(name):
        raise ValueError(f"invalid identifier: {name}")
    return '"' + name + '"'


def batch_insert(db_path: str, table: str, rows: list[dict]) -> int:
    if not rows:
        return 0

    quoted_table = _quote_ident(table)
    cols = list(rows[0].keys())
    quoted_cols = [_quote_ident(c) for c in cols]
    col_set = set(cols)

    values = []
    for row in rows:
        if set(row.keys()) != col_set:
            raise RuntimeError(
                f"row keys {sorted(row.keys())} do not match columns {sorted(cols)}"
            )
        values.append([row[c] for c in cols])

    col_str = ", ".join(quoted_cols)
    placeholders = ", ".join("?" for _ in cols)
    sql = f"INSERT INTO {quoted_table} ({col_str}) VALUES ({placeholders})"

    conn = sqlite3.connect(db_path)
    try:
        conn.executemany(sql, values)
        conn.commit()
        return len(rows)
    except sqlite3.Error as exc:
        conn.rollback()
        raise RuntimeError(f"batch insert failed: {exc}") from exc
    finally:
        conn.close()
