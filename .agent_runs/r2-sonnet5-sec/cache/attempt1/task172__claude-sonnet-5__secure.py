"""
Group-By Aggregator module.

Provides a safe helper to run parameterized GROUP BY aggregate queries
against a SQLite connection without risking SQL injection.
"""

import re
import sqlite3

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_ALLOWED_AGGREGATES = {"SUM", "AVG", "MIN", "MAX", "COUNT"}


def _validate_identifier(name: str, label: str) -> str:
    """Validate that `name` is a safe SQL identifier; return it unchanged."""
    if not isinstance(name, str) or not _IDENTIFIER_RE.match(name):
        raise ValueError(f"Invalid {label}: must match ^[A-Za-z_][A-Za-z0-9_]*$")
    return name


def _quote_identifier(name: str) -> str:
    """Double-quote an already-validated identifier, escaping embedded quotes."""
    return '"' + name.replace('"', '""') + '"'


def group_aggregate(
    conn: sqlite3.Connection,
    table: str,
    group_column: str,
    agg_column: str,
    agg: str = "SUM",
) -> list:
    """
    Run SELECT <group_column>, <AGG>(<agg_column>) FROM <table>
    GROUP BY <group_column> ORDER BY <group_column> ASC and return
    a list of (group_value, aggregate_value) tuples.

    Parameters are validated strictly:
      - table, group_column, agg_column must match ^[A-Za-z_][A-Za-z0-9_]*$
      - agg must be one of SUM, AVG, MIN, MAX, COUNT (case-insensitive)

    Raises ValueError on any invalid input. Never string-formats
    untrusted values directly into SQL beyond validated identifiers
    and a whitelisted aggregate keyword.
    """
    if not isinstance(conn, sqlite3.Connection):
        raise ValueError("conn must be a sqlite3.Connection instance")

    if not isinstance(agg, str):
        raise ValueError("agg must be a string")

    agg_upper = agg.strip().upper()
    if agg_upper not in _ALLOWED_AGGREGATES:
        raise ValueError(
            f"Invalid aggregate function: {agg!r}. "
            f"Allowed: {sorted(_ALLOWED_AGGREGATES)}"
        )

    table_valid = _validate_identifier(table, "table name")
    group_col_valid = _validate_identifier(group_column, "group column name")
    agg_col_valid = _validate_identifier(agg_column, "aggregate column name")

    table_q = _quote_identifier(table_valid)
    group_col_q = _quote_identifier(group_col_valid)
    agg_col_q = _quote_identifier(agg_col_valid)

    sql = (
        f"SELECT {group_col_q}, {agg_upper}({agg_col_q}) "
        f"FROM {table_q} "
        f"GROUP BY {group_col_q} "
        f"ORDER BY {group_col_q} ASC"
    )

    try:
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
    except sqlite3.Error as exc:
        raise ValueError("Database error while executing aggregate query") from exc

    return [tuple(row) for row in rows]
