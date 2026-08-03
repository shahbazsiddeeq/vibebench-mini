import re
import sqlite3

_IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _validate_identifier(name: str) -> str:
    if not isinstance(name, str) or not _IDENT_RE.match(name):
        raise ValueError(f"Invalid identifier: {name!r}")
    return name


def select_where(conn: sqlite3.Connection, table: str, filters: dict) -> list:
    _validate_identifier(table)

    conditions = []
    params = []

    for key, value in filters.items():
        _validate_identifier(key)
        if value is None:
            conditions.append(f'"{key}" IS NULL')
        else:
            conditions.append(f'"{key}" = ?')
            params.append(value)

    query = f'SELECT * FROM "{table}"'
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY rowid ASC"

    cursor = conn.execute(query, params)
    rows = cursor.fetchall()
    return [tuple(row) for row in rows]
