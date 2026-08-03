import sqlite3
import re


def select_where(conn: sqlite3.Connection, table: str, filters: dict) -> list[tuple]:
    """
    SELECT * FROM <table> filtering rows where every key equals its value.
    
    Args:
        conn: SQLite database connection
        table: Table name (must be valid identifier)
        filters: Dictionary of column_name: value pairs
        
    Returns:
        List of tuples representing matching rows, ordered by rowid ascending
        
    Raises:
        ValueError: If table name or any filter key is not a valid identifier
    """
    # Regex pattern for valid SQL identifiers
    identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    
    # Validate table name
    if not identifier_pattern.match(table):
        raise ValueError(f"Invalid table identifier: {table}")
    
    # Validate all filter keys
    for key in filters.keys():
        if not identifier_pattern.match(key):
            raise ValueError(f"Invalid column identifier: {key}")
    
    # Build the SQL query
    # Quote the table name
    quoted_table = f'"{table}"'
    
    # Start building the query
    query = f"SELECT * FROM {quoted_table}"
    
    # Build WHERE clause if filters exist
    params = []
    if filters:
        conditions = []
        for col, value in filters.items():
            quoted_col = f'"{col}"'
            if value is None:
                # Use IS NULL for None values
                conditions.append(f"{quoted_col} IS ?")
            else:
                # Use = for other values
                conditions.append(f"{quoted_col} = ?")
            params.append(value)
        
        query += " WHERE " + " AND ".join(conditions)
    
    # Add ORDER BY rowid
    query += " ORDER BY rowid ASC"
    
    # Execute query with bound parameters
    cursor = conn.execute(query, params)
    results = cursor.fetchall()
    
    return results
