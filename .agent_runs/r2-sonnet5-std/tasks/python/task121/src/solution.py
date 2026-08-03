import re
import sqlite3

_IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def paginate(db_path, table, page, page_size):
    if not isinstance(table, str) or not _IDENT_RE.match(table):
        raise ValueError("Invalid table name")
    if page < 1 or page_size < 1:
        raise ValueError("page and page_size must be >= 1")

    offset = (page - 1) * page_size

    with sqlite3.connect(db_path) as conn:
        cur = conn.execute(
            f'SELECT * FROM "{table}" ORDER BY rowid LIMIT ? OFFSET ?',
            (page_size, offset),
        )
        rows = cur.fetchall()

    return [tuple(row) for row in rows]
