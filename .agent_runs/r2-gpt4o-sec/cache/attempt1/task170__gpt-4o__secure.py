import sqlite3
import re

def select_where(conn: sqlite3.Connection, table: str, filters: dict) -> list[tuple]:
    # Regex pattern for valid SQL identifiers
    identifier_pattern = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

    # Validate table name
    if not identifier_pattern.match(table):
        raise ValueError("Invalid table name")

    # Validate filter keys
    for key in filters.keys():
        if not identifier_pattern.match(key):
            raise ValueError(f"Invalid column name: {key}")

    # Start building the SQL query
    query = f'SELECT * FROM "{table}"'
    params = []

    # Add WHERE clause if filters are provided
    if filters:
        conditions = []
        for key, value in filters.items():
            if value is None:
                conditions.append(f'"{key}" IS NULL')
            else:
                conditions.append(f'"{key}" = ?')
                params.append(value)
        query += " WHERE " + " AND ".join(conditions)

    # Order by rowid to ensure consistent ordering
    query += " ORDER BY rowid ASC"

    # Execute the query and fetch results
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()

    return results
