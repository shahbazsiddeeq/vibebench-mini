import sqlite3
import re
from typing import Any


def select_where(conn: sqlite3.Connection, table: str, filters: dict) -> list[tuple]:
    """
    Execute SELECT * FROM <table> with optional WHERE filters.
    
    Args:
        conn: sqlite3 connection
        table: table name (validated as identifier)
        filters: dict of column_name -> value pairs for WHERE clause
        
    Returns:
        List of tuples representing rows, ordered by rowid ascending
        
    Raises:
        ValueError: if table name or any filter key is not a valid identifier
    """
    # Validate table name as identifier
    if not _is_valid_identifier(table):
        raise ValueError(f"Invalid table identifier: {table}")
    
    # Validate all filter keys as identifiers
    for key in filters.keys():
        if not _is_valid_identifier(key):
            raise ValueError(f"Invalid column identifier: {key}")
    
    # Build the SQL query
    quoted_table = f'"{table}"'
    
    if not filters:
        # No filters - return all rows
        query = f"SELECT * FROM {quoted_table} ORDER BY rowid ASC"
        cursor = conn.execute(query)
    else:
        # Build WHERE clause with bound parameters
        where_parts = []
        params = []
        
        for key, value in filters.items():
            quoted_key = f'"{key}"'
            if value is None:
                # Use IS NULL for None values
                where_parts.append(f"{quoted_key} IS NULL")
            else:
                # Use = with bound parameter for other values
                where_parts.append(f"{quoted_key} = ?")
                params.append(value)
        
        where_clause = " AND ".join(where_parts)
        query = f"SELECT * FROM {quoted_table} WHERE {where_clause} ORDER BY rowid ASC"
        cursor = conn.execute(query, params)
    
    # Fetch all results as list of tuples
    return cursor.fetchall()


def _is_valid_identifier(name: str) -> bool:
    """
    Check if a name is a valid SQL identifier.
    Must match: ^[A-Za-z_][A-Za-z0-9_]*$
    
    Args:
        name: identifier to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r"^[A-Za-z_][A-Za-z0-9_]*$"
    return bool(re.match(pattern, name))
