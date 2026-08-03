import sqlite3
import re
from typing import Any


def select_where(conn: sqlite3.Connection, table: str, filters: dict) -> list[tuple]:
    """
    Select rows from a table with optional filtering.
    
    Args:
        conn: sqlite3 connection
        table: table name (validated as identifier)
        filters: dict of column_name -> value pairs for filtering
        
    Returns:
        list of tuples representing matching rows, ordered by rowid ascending
        
    Raises:
        ValueError: if table name or any filter key is not a valid identifier
    """
    # Validate identifier pattern
    identifier_pattern = r'^[A-Za-z_][A-Za-z0-9_]*$'
    
    # Validate table name
    if not re.match(identifier_pattern, table):
        raise ValueError(f"Invalid table identifier: {table}")
    
    # Validate all filter keys
    for key in filters.keys():
        if not re.match(identifier_pattern, key):
            raise ValueError(f"Invalid column identifier: {key}")
    
    # Build the SQL query
    query = f'SELECT * FROM "{table}"'
    
    # Build WHERE clause if filters exist
    if filters:
        where_conditions = []
        params = []
        
        for key, value in filters.items():
            if value is None:
                # Use IS NULL for None values
                where_conditions.append(f'"{key}" IS NULL')
            else:
                # Use = with bound parameter for other values
                where_conditions.append(f'"{key}" = ?')
                params.append(value)
        
        query += ' WHERE ' + ' AND '.join(where_conditions)
    else:
        params = []
    
    # Add ordering by rowid
    query += ' ORDER BY rowid ASC'
    
    # Execute and return results
    cursor = conn.execute(query, params)
    return cursor.fetchall()
