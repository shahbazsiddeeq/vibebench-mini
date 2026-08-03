import re
import sqlite3

_IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _quote_identifier(name):
    """Validate an identifier against a strict whitelist and double-quote it."""
    if not isinstance(name, str) or not _IDENT_RE.match(name):
        raise ValueError(f"invalid SQL identifier: {name!r}")
    return '"' + name.replace('"', '""') + '"'


def select_where(conn, table, filters):
    """Return rows of ``table`` matching every ``filters`` entry (AND).

    Values are always bound parameters; identifiers are whitelist-validated
    and double-quoted. Rows are returned as tuples ordered by rowid ascending.
    """
    if not isinstance(filters, dict):
        raise ValueError("filters must be a dict")

    table_sql = _quote_identifier(table)

    where_clauses = []
    params = []
    for column, value in filters.items():
        col_sql = _quote_identifier(column)
        if value is None:
            where_clauses.append(f"{col_sql} IS NULL")
        else:
            where_clauses.append(f"{col_sql} = ?")
            params.append(value)

    sql = f"SELECT * FROM {table_sql}"
    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)
    sql += " ORDER BY rowid ASC"

    cur = conn.execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    return [tuple(r) for r in rows]
