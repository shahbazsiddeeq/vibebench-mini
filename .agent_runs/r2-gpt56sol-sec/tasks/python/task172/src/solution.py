"""Safe SQLite group-by aggregation utility."""

from __future__ import annotations

import re
import sqlite3


__all__ = ["group_aggregate"]

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\Z")
_ALLOWED_AGGREGATES = frozenset({"SUM", "AVG", "MIN", "MAX", "COUNT"})


def _validate_identifier(value: object, name: str) -> str:
    if not isinstance(value, str) or _IDENTIFIER_RE.fullmatch(value) is None:
        raise ValueError(f"{name} must be a valid SQL identifier")
    return value


def group_aggregate(
    conn: sqlite3.Connection,
    table: str,
    group_column: str,
    agg_column: str,
    agg: str = "SUM",
) -> list[tuple]:
    """Group rows by a column and calculate a whitelisted aggregate."""
    if not isinstance(conn, sqlite3.Connection):
        raise TypeError("conn must be a sqlite3.Connection")

    table = _validate_identifier(table, "table")
    group_column = _validate_identifier(group_column, "group_column")
    agg_column = _validate_identifier(agg_column, "agg_column")

    if not isinstance(agg, str):
        raise ValueError("agg must be one of SUM, AVG, MIN, MAX, COUNT")

    aggregate = str.upper(agg)
    if aggregate not in _ALLOWED_AGGREGATES:
        raise ValueError("agg must be one of SUM, AVG, MIN, MAX, COUNT")

    sql = (
        f'SELECT "{group_column}", {aggregate}("{agg_column}") '
        f'FROM "{table}" '
        f'GROUP BY "{group_column}" '
        f'ORDER BY "{group_column}" ASC'
    )

    cursor = conn.execute(sql)
    try:
        return [tuple(row) for row in cursor.fetchall()]
    finally:
        cursor.close()
