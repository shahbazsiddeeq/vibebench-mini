import sqlite3
import re
from collections.abc import Collection

def fetch_sorted(conn: sqlite3.Connection, table: str, sort_column: str, allowed_columns: Collection[str], descending: bool = False, limit: int | None = None) -> list[tuple]:
    """
    Runs SELECT * FROM <table> ORDER BY <sort_column> [ASC|DESC] with an optional LIMIT
    and returns rows as a list of tuples (columns in the table's definition order).

    sort_column MUST be present in allowed_columns (membership check) OR the call raises ValueError.
    table and sort_column are IDENTIFIERS that must match ^[A-Za-z_][A-Za-z0-9_]*$
    and are double-quoted when built into SQL (ValueError otherwise).
    Sort direction comes from the boolean descending (True -> DESC, False -> ASC).
    limit, when not None, must be a non-negative int and is passed as a bound parameter (?);
    a negative or non-int limit raises ValueError.
    Do not close the passed-in connection.
    Ordering ties are broken by rowid ascending so results are deterministic.
    """

    identifier_pattern = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

    # Validate table name
    if not isinstance(table, str) or not identifier_pattern.fullmatch(table):
        raise ValueError("Invalid table name. Must be a valid SQL identifier.")

    # Validate sort_column
    if not isinstance(sort_column, str) or not identifier_pattern.fullmatch(sort_column):
        raise ValueError("Invalid sort_column name. Must be a valid SQL identifier.")

    if sort_column not in allowed_columns:
        raise ValueError(f"Sort column '{sort_column}' is not in the allowed list.")

    # Validate limit
    limit_param = None
    if limit is not None:
        if not isinstance(limit, int) or limit < 0:
            raise ValueError("Limit must be a non-negative integer or None.")
        limit_param = limit

    # Build SQL query
    quoted_table = f'"{table}"'
    quoted_sort_column = f'"{sort_column}"'
    sort_order = "DESC" if descending else "ASC"

    sql_query = f"SELECT * FROM {quoted_table} ORDER BY {quoted_sort_column} {sort_order}, rowid ASC"

    params = []
    if limit_param is not None:
        sql_query += " LIMIT ?"
        params.append(limit_param)

    try:
        cursor = conn.execute(sql_query, params)
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        # Log the error internally if possible, but for this task,
        # re-raising a generic error or specific ValueError is sufficient
        # to avoid exposing internal database details.
        raise ValueError(f"Database error during query execution: {e}") from e
