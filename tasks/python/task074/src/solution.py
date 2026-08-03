from __future__ import annotations

import re
import sqlite3

_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _quote_ident(name: str) -> str:
    if not _IDENT.match(name):
        raise ValueError(f"invalid identifier: {name}")
    return '"' + name + '"'


def upsert(db_path: str, table: str, record: dict, key: str) -> None:
    if key not in record:
        raise KeyError(f"key '{key}' not in record")

    quoted_table = _quote_ident(table)
    quoted_key = _quote_ident(key)
    quoted_cols = {k: _quote_ident(k) for k in record}

    cols = ", ".join(quoted_cols[k] for k in record)
    placeholders = ", ".join("?" for _ in record)
    non_key = [k for k in record if k != key]
    if non_key:
        updates = ", ".join(
            f"{quoted_cols[k]}=excluded.{quoted_cols[k]}" for k in non_key
        )
        conflict_action = f"DO UPDATE SET {updates}"
    else:
        # Record carries only the conflict key: nothing to update.
        conflict_action = "DO NOTHING"

    sql = (
        f"INSERT INTO {quoted_table} ({cols}) VALUES ({placeholders}) "
        f"ON CONFLICT({quoted_key}) {conflict_action}"
    )

    conn = sqlite3.connect(db_path)
    try:
        conn.execute(sql, list(record.values()))
        conn.commit()
    finally:
        conn.close()
