import re
import sqlite3
from typing import Any


_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _quote_identifier(identifier: str) -> str:
    if not isinstance(identifier, str) or _IDENTIFIER_RE.fullmatch(identifier) is None:
        raise ValueError(f"Invalid SQL identifier: {identifier!r}")
    return f'"{identifier}"'


def select_where(
    conn: sqlite3.Connection,
    table: str,
    filters: dict[str, Any],
) -> list[tuple]:
    quoted_table = _quote_identifier(table)

    clauses: list[str] = []
    parameters: list[Any] = []

    for column, value in filters.items():
        quoted_column = _quote_identifier(column)
        if value is None:
            clauses.append(f"{quoted_column} IS ?")
        else:
            clauses.append(f"{quoted_column} = ?")
        parameters.append(value)

    sql = f"SELECT * FROM {quoted_table}"
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY rowid ASC"

    cursor = conn.cursor()
    try:
        cursor.row_factory = None
        cursor.execute(sql, parameters)
        return [tuple(row) for row in cursor.fetchall()]
    finally:
        cursor.close()
