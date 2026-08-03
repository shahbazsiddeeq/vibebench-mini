import re
import sqlite3
from collections.abc import Collection

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def fetch_sorted(
    conn: sqlite3.Connection,
    table: str,
    sort_column: str,
    allowed_columns: Collection[str],
    descending: bool = False,
    limit: int | None = None,
) -> list[tuple]:
    try:
        allowed = sort_column in allowed_columns
    except (TypeError, AttributeError):
        raise ValueError("sort_column must be present in allowed_columns") from None

    if not allowed:
        raise ValueError("sort_column must be present in allowed_columns")

    if not isinstance(table, str) or _IDENTIFIER_RE.fullmatch(table) is None:
        raise ValueError("invalid table identifier")
    if not isinstance(sort_column, str) or _IDENTIFIER_RE.fullmatch(sort_column) is None:
        raise ValueError("invalid sort_column identifier")

    if limit is not None and (type(limit) is not int or limit < 0):
        raise ValueError("limit must be a non-negative integer or None")

    direction = "DESC" if descending else "ASC"
    sql = (
        f'SELECT * FROM "{table}" '
        f'ORDER BY "{sort_column}" {direction}, rowid ASC'
    )
    parameters: tuple[int, ...] = ()

    if limit is not None:
        sql += " LIMIT ?"
        parameters = (limit,)

    cursor = conn.execute(sql, parameters)
    try:
        return [tuple(row) for row in cursor.fetchall()]
    finally:
        cursor.close()
