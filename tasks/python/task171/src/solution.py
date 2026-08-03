import re
import sqlite3

_IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _quote_identifier(name):
    if not isinstance(name, str) or not _IDENT_RE.match(name):
        raise ValueError(f"invalid SQL identifier: {name!r}")
    return '"' + name.replace('"', '""') + '"'


def fetch_sorted(conn, table, sort_column, allowed_columns, descending=False, limit=None):
    """Return all rows of ``table`` sorted by ``sort_column``.

    ``sort_column`` must be a member of ``allowed_columns`` (whitelist) and a
    valid identifier. Direction is chosen by the ``descending`` boolean, not by
    any user string. ``limit`` is bound as a parameter.
    """
    if sort_column not in allowed_columns:
        raise ValueError(f"column not allowed for sorting: {sort_column!r}")

    table_sql = _quote_identifier(table)
    col_sql = _quote_identifier(sort_column)
    direction = "DESC" if descending else "ASC"

    sql = f"SELECT * FROM {table_sql} ORDER BY {col_sql} {direction}, rowid ASC"

    params = []
    if limit is not None:
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
            raise ValueError(f"invalid limit: {limit!r}")
        sql += " LIMIT ?"
        params.append(limit)

    cur = conn.execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    return [tuple(r) for r in rows]
