import sqlite3
import re
from typing import Collection, Optional, List, Tuple

def _validate_identifier(identifier: str, name: str) -> None:
    """Validates if the identifier matches the allowed pattern."""
    if not re.fullmatch(r"^[A-Za-z_][A-Za-z0-9_]*$", identifier):
        raise ValueError(f"Invalid {name} identifier: '{identifier}'")

def fetch_sorted(
    conn: sqlite3.Connection,
    table: str,
    sort_column: str,
    allowed_columns: Collection[str],
    descending: bool = False,
    limit: Optional[int] = None,
) -> List[Tuple]:
    """
    Runs SELECT * FROM <table> ORDER BY <sort_column> [ASC|DESC] with an optional LIMIT
    and returns rows as a list of tuples (columns in the table's definition order).

    sort_column MUST be present in allowed_columns (membership check) OR the call raises ValueError;
    this whitelist is the primary defense so that only caller-approved columns can appear in ORDER BY.
    In addition, table and sort_column are IDENTIFIERS that must match ^[A-Za-z_][A-Za-z0-9_]*$
    and are double-quoted when built into SQL (ValueError otherwise).
    Sort direction comes from the boolean descending (True -> DESC, False -> ASC);
    it is never taken from a string.
    limit, when not None, must be a non-negative int and is passed as a bound parameter (?);
    a negative or non-int limit raises ValueError.
    Do not close the passed-in connection.
    Ordering ties are broken by rowid ascending so results are deterministic.
    """

    _validate_identifier(table, "table")
    _validate_identifier(sort_column, "sort_column")

    if sort_column not in allowed_columns:
        raise ValueError(
            f"Sort column '{sort_column}' is not in the allowed columns."
        )

    order_direction = "DESC" if descending else "ASC"

    query_parts = [
        f'SELECT * FROM "{table}"',
        f'ORDER BY "{sort_column}" {order_direction}, rowid ASC',
    ]
    params: List[int] = []

    if limit is not None:
        if not isinstance(limit, int) or limit < 0:
            raise ValueError(
                f"Limit must be a non-negative integer or None, got {limit}."
            )
        query_parts.append("LIMIT ?")
        params.append(limit)

    sql_query = " ".join(query_parts)

    cursor = conn.execute(sql_query, params)
    return cursor.fetchall()
