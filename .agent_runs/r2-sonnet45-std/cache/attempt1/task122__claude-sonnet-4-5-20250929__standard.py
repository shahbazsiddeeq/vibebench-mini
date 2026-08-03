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
        Dict mapping values to their counts
    
    Raises:
        ValueError: If table or column is an invalid identifier
    """
    # Validate that table and column are valid SQL identifiers
    # Valid identifiers: start with letter or underscore, contain only alphanumeric and underscore
    identifier_pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
    
    if not identifier_pattern.match(table):
        raise ValueError(f"Invalid table identifier: {table}")
    
    if not identifier_pattern.match(column):
        raise ValueError(f"Invalid column identifier: {column}")
    
    # Connect to database and execute query
    with sqlite3.connect(db_path) as conn:
        # Use validated identifiers directly in query (safe after validation)
        query = f"SELECT {column}, COUNT(*) FROM {table} GROUP BY {column}"
        cursor = conn.execute(query)
        
        # Build result dictionary
        result = {}
        for value, count in cursor.fetchall():
            result[value] = count
        
        return result
