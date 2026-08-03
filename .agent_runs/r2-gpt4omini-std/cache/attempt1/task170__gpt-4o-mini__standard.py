import sqlite3
import re
from typing import List, Tuple, Dict

def select_where(conn: sqlite3.Connection, table: str, filters: Dict[str, any]) -> List[Tuple]:
    # Validate table name
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', table):
        raise ValueError("Invalid table name")

    # Prepare the SQL query
    query = f'SELECT * FROM "{table}"'
    conditions = []
    parameters = []

    for key, value in filters.items():
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', key):
            raise ValueError(f"Invalid filter key: {key}")
        
        if value is None:
            conditions.append(f'"{key}" IS ?')
            parameters.append(None)
        else:
            conditions.append(f'"{key}" = ?')
            parameters.append(value)

    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)

    query += ' ORDER BY rowid ASC'

    # Execute the query with parameters
    cursor = conn.execute(query, parameters)
    return cursor.fetchall()
