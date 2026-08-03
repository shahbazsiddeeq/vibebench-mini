import re
import sqlite3

_IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_ALLOWED_AGGS = {"SUM", "AVG", "MIN", "MAX", "COUNT"}


def _quote_identifier(name):
    if not isinstance(name, str) or not _IDENT_RE.match(name):
        raise ValueError(f"invalid SQL identifier: {name!r}")
    return '"' + name.replace('"', '""') + '"'


def group_aggregate(conn, table, group_column, agg_column, agg="SUM"):
    """Group ``table`` by ``group_column`` and aggregate ``agg_column``.

    ``agg`` is whitelist-validated (SUM/AVG/MIN/MAX/COUNT, case-insensitive).
    Identifiers are validated and double-quoted. Returns a list of
    ``(group_value, aggregate_value)`` tuples ordered by group_value ascending
    (NULLs first).
    """
    if not isinstance(agg, str):
        raise ValueError(f"invalid aggregate: {agg!r}")
    agg_upper = agg.upper()
    if agg_upper not in _ALLOWED_AGGS:
        raise ValueError(f"aggregate not allowed: {agg!r}")

    table_sql = _quote_identifier(table)
    group_sql = _quote_identifier(group_column)
    agg_col_sql = _quote_identifier(agg_column)

    sql = (
        f"SELECT {group_sql}, {agg_upper}({agg_col_sql}) "
        f"FROM {table_sql} GROUP BY {group_sql} ORDER BY {group_sql} ASC"
    )

    cur = conn.execute(sql)
    rows = cur.fetchall()
    cur.close()
    return [tuple(r) for r in rows]
