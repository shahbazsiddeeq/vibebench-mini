import sqlite3
import re

def _validate_identifier(identifier: str):
    """
    Validates if the given string is a valid SQL identifier.
    Raises ValueError if it's not.
    """
    if not re.fullmatch(r"^[A-Za-z_][A-Za-z0-9_]*$", identifier):
        raise ValueError(f"Invalid identifier: '{identifier}'")

def select_where(conn: sqlite3.Connection, table: str, filters: dict) -> list[tuple]:
    """
    Runs SELECT * FROM <table> filtering rows where every key equals its value,
    combined with AND, and returns the resulting rows as a list of tuples
    (columns in the table's definition order) ordered by rowid ascending.
    All filter VALUES must be passed as bound parameters (never string-formatted).
    The table name and every filter key are IDENTIFIERS: each must match the regex
    ^[A-Za-z_][A-Za-z0-9_]*$ and is then wrapped in double quotes when built into SQL;
    if any identifier fails the regex, raise ValueError (this blocks SQL injection).
    An empty filters dict returns all rows. A filter value of None matches rows where
    that column IS NULL (uses `IS ?` semantics via `col IS NULL` when the value is None).
    Do not close the passed-in connection.
    """
    _validate_identifier(table)
    quoted_table = f'"{table}"'

    where_clauses = []
    params = []

    for key, value in filters.items():
        _validate_identifier(key)
        quoted_key = f'"{key}"'

        if value is None:
            where_clauses.append(f"{quoted_key} IS NULL")
        else:
            where_clauses.append(f"{quoted_key} = ?")
            params.append(value)

    sql = f"SELECT * FROM {quoted_table}"
    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)
    sql += " ORDER BY rowid ASC"

    cursor = conn.execute(sql, params)
    return cursor.fetchall()
