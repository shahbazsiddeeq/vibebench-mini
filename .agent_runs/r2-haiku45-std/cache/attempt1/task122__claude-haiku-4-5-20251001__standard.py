import sqlite3
import re


def value_counts(db_path, table, column):
    """
    Returns a dict mapping each distinct value in the given column to its count.
    
    Args:
        db_path: Path to the SQLite database
        table: Table name
        column: Column name
        
    Returns:
        Dict mapping distinct values to their counts
        
    Raises:
        ValueError: If table or column is an invalid identifier
    """
    # Validate table and column names as identifiers
    # Valid identifiers: alphanumeric, underscore, start with letter or underscore
    identifier_pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    
    if not re.match(identifier_pattern, table):
        raise ValueError(f"Invalid table name: {table}")
    
    if not re.match(identifier_pattern, column):
        raise ValueError(f"Invalid column name: {column}")
    
    # Connect to database and execute query
    with sqlite3.connect(db_path) as conn:
        # Use parameterized query for safety, but identifiers must be in query string
        # since they can't be parameterized
        query = f"SELECT {column}, COUNT(*) as count FROM {table} GROUP BY {column}"
        
        try:
            cursor = conn.execute(query)
            result = {}
            for row in cursor:
                value, count = row
                result[value] = count
            return result
        except sqlite3.OperationalError as e:
            # If table or column doesn't exist, raise ValueError
            raise ValueError(f"Invalid table or column: {e}")
