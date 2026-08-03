import re
import sqlite3

_IDENTIFIER_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
_VALID_AGGS = {'SUM', 'AVG', 'MIN', 'MAX', 'COUNT'}


def _validate_identifier(name: str) -> str:
    if not isinstance(name, str) or not _IDENTIFIER_RE.match(name):
        raise ValueError(f"Invalid identifier: {name!r}")
    return name


def group_aggregate(
    conn: sqlite3.Connection,
    table: str,
    group_column: str,
    agg_column: str,
    agg: str = 'SUM',
) -> list:
    if not isinstance(agg, str):
        raise ValueError(f"Invalid aggregate function: {agg!r}")
    agg_upper = agg.upper()
    if agg_upper not in _VALID_AGGS:
        raise ValueError(f"Invalid aggregate function: {agg!r}")

    table = _validate_identifier(table)
    group_column = _validate_identifier(group_column)
    agg_column = _validate_identifier(agg_column)

    query = (
        f'SELECT "{group_column}", {agg_upper}("{agg_column}") '
        f'FROM "{table}" GROUP BY "{group_column}" ORDER BY "{group_column}" ASC'
    )

    cursor = conn.execute(query)
    try:
        rows = cursor.fetchall()
    finally:
        cursor.close()

    return [tuple(row) for row in rows]
