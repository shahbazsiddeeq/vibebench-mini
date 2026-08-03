import re
import sqlite3

__all__ = ["group_aggregate"]

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_ALLOWED_AGGREGATES = {"SUM", "AVG", "MIN", "MAX", "COUNT"}


def group_aggregate(
    conn: sqlite3.Connection,
    table: str,
    group_column: str,
    agg_column: str,
    agg: str = "SUM",
) -> list[tuple]:
    if not isinstance(agg, str) or agg.upper() not in _ALLOWED_AGGREGATES:
        raise ValueError("agg must be one of SUM, AVG, MIN, MAX, or COUNT")

    identifiers = {
        "table": table,
        "group_column": group_column,
        "agg_column": agg_column,
    }
    for name, identifier in identifiers.items():
        if not isinstance(identifier, str) or _IDENTIFIER_RE.fullmatch(identifier) is None:
            raise ValueError(f"invalid {name} identifier")

    aggregate = agg.upper()
    sql = (
        f'SELECT "{group_column}", {aggregate}("{agg_column}") '
        f'FROM "{table}" '
        f'GROUP BY "{group_column}" '
        f'ORDER BY "{group_column}" ASC'
    )
    return list(conn.execute(sql).fetchall())
