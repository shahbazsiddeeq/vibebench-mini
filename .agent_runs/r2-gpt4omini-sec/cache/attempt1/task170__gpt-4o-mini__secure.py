import sqlite3
import re
from typing import List, Tuple, Dict, Any

def validate_identifier(identifier: str) -> None:
    """Validate that the identifier matches the required regex."""
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', identifier):
        raise ValueError(f"Invalid identifier: {identifier}")

def select_where(conn: sqlite3.Connection, table: str, filters: Dict[str, Any]) -> List[Tuple]:
    """Select rows from a table with given filters."""
    validate_identifier(table)
    
    # Prepare the base query
    query = f'SELECT * FROM "{table}"'
    conditions = []
    parameters = []

    for key, value in filters.items():
        validate_identifier(key)
        if value is None:
            conditions.append(f'"{key}" IS ?')
            parameters.append(None)
        else:
            conditions.append(f'"{key}" = ?')
            parameters.append(value)

    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)

    query += ' ORDER BY rowid ASC'

    # Execute the query and fetch results
    cursor = conn.execute(query, parameters)
    return cursor.fetchall()
