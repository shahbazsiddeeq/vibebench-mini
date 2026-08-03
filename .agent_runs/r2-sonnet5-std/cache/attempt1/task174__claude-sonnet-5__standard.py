import re
import sqlite3

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _validate_identifier(name: str) -> str:
    if not isinstance(name, str) or not _IDENTIFIER_RE.match(name):
        raise ValueError(f"Invalid identifier: {name!r}")
    return name


def bulk_update(conn: sqlite3.Connection, table: str, key_column: str, rows: list) -> int:
    if not isinstance(rows, list):
        raise ValueError("rows must be a list")

    _validate_identifier(table)
    _validate_identifier(key_column)

    if not rows:
        return 0

    statements = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("each row must be a dict")
        if key_column not in row:
            raise ValueError(f"row missing key column: {key_column}")

        set_cols = [c for c in row.keys() if c != key_column]
        if not set_cols:
            raise ValueError("row must have at least one column to set besides key_column")

        for c in set_cols:
            _validate_identifier(c)

        set_clause = ", ".join(f'"{c}" = ?' for c in set_cols)
        sql = f'UPDATE "{table}" SET {set_clause} WHERE "{key_column}" = ?'
        params = [row[c] for c in set_cols] + [row[key_column]]
        statements.append((sql, params))

    total = 0
    cur = conn.cursor()
    try:
        for sql, params in statements:
            cur.execute(sql, params)
            total += cur.rowcount
        conn.commit()
    except Exception:
        conn.rollback()
        raise

    return total
