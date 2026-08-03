import re
import sqlite3

_IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def fetch_sorted(conn: sqlite3.Connection, table: str, sort_column: str,
                  allowed_columns, descending: bool = False,
                  limit=None) -> list:
    if sort_column not in allowed_columns:
        raise ValueError(f"sort_column {sort_column!r} not in allowed_columns")

    if not isinstance(table, str) or not _IDENT_RE.match(table):
        raise ValueError(f"invalid table identifier: {table!r}")

    if not isinstance(sort_column, str) or not _IDENT_RE.match(sort_column):
        raise ValueError(f"invalid sort_column identifier: {sort_column!r}")

    if not isinstance(descending, bool):
        raise ValueError("descending must be a bool")

    direction = "DESC" if descending else "ASC"

    params = []
    limit_clause = ""
    if limit is not None:
        if not isinstance(limit, int) or isinstance(limit, bool) or limit < 0:
            raise ValueError("limit must be a non-negative int")
        limit_clause = " LIMIT ?"
        params.append(limit)

    query = (
        f'SELECT * FROM "{table}" '
        f'ORDER BY "{sort_column}" {direction}, rowid ASC'
        f'{limit_clause}'
    )

    cur = conn.execute(query, params)
    try:
        rows = cur.fetchall()
    finally:
        cur.close()

    return [tuple(row) for row in rows]
