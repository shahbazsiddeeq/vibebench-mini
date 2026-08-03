import sqlite3
import re

def select_where(conn: sqlite3.Connection, table: str, filters: dict) -> list[tuple]:
    """
    Runs SELECT * FROM <table> filtering rows where every key equals its value,
    combined with AND, and returns the resulting rows as a list of tuples
    (columns in the table's definition order) ordered by rowid ascending.
    
    Args:
        conn: SQLite database connection
        table: Table name (must be a valid identifier)
        filters: Dictionary of column names to values for filtering
        
    Returns:
        List of tuples representing matching rows
        
    Raises:
        ValueError: If table name or any filter key is not a valid identifier
    """
    # Regex pattern for valid SQL identifiers
    identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    
    # Validate table name
    if not identifier_pattern.match(table):
        raise ValueError(f"Invalid table identifier: {table}")
    
    # Validate all filter keys (column names)
    for key in filters.keys():
        if not identifier_pattern.match(key):
            raise ValueError(f"Invalid column identifier: {key}")
    
    # Build the SQL query
    # Wrap table name in double quotes for safety
    query = f'SELECT * FROM "{table}"'
    
    # Build WHERE clause if filters exist
    params = []
    if filters:
        where_clauses = []
        for col, value in filters.items():
            # Wrap column name in double quotes
            if value is None:
                # Use IS NULL for None values
                where_clauses.append(f'"{col}" IS NULL')
            else:
                # Use = ? for other values
                where_clauses.append(f'"{col}" = ?')
                params.append(value)
        
        query += ' WHERE ' + ' AND '.join(where_clauses)
    
    # Add ORDER BY rowid
    query += ' ORDER BY rowid ASC'
    
    # Execute query with bound parameters
    cursor = conn.execute(query, params)
    results = cursor.fetchall()
    
    return results
