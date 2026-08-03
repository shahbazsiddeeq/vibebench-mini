import sqlite3
import re

def _validate_identifier(identifier: str):
    """Validates if the identifier matches the allowed regex."""
    if not re.fullmatch(r"^[A-Za-z_][A-Za-z0-9_]*$", identifier):
        raise ValueError(f"Invalid identifier: '{identifier}'")

def select_where(conn: sqlite3.Connection, table: str, filters: dict) -> list[tuple]:
    """
    Runs SELECT * FROM <table> filtering rows where every key equals its value,
    combined with AND, and returns the resulting rows as a list of tuples
    ordered by rowid ascending.

    All filter VALUES must be passed as bound parameters.
    The table name and every filter key are IDENTIFIERS: each must match the
    regex ^[A-Za-z_][A-Za-z0-9_]*$ and is then wrapped in double quotes when
    built into SQL; if any identifier fails the regex, raise ValueError.
    An empty filters dict returns all rows.
    A filter value of None matches rows where that column IS NULL.
    Does not close the passed-in connection.
    """
    _validate_identifier(table)
    quoted_table = f'"{table}"'

    query_parts = []
    params = []

    for key, value in filters.items():
        _validate_identifier(key)
        quoted_key = f'"{key}"'

        if value is None:
            query_parts.append(f"{quoted_key} IS NULL")
        else:
            query_parts.append(f"{quoted_key} = ?")
            params.append(value)

    sql_query = f"SELECT * FROM {quoted_table}"
    if query_parts:
        sql_query += " WHERE " + " AND ".join(query_parts)
    sql_query += " ORDER BY rowid ASC"

    try:
        cursor = conn.execute(sql_query, params)
        return cursor.fetchall()
    except sqlite3.Error as e:
        # Log the error internally if a logging mechanism were available.
        # For this problem, re-raising a generic error or specific ValueError
        # is appropriate to avoid exposing internal database details.
        raise RuntimeError(f"Database error during query execution: {e}") from e
