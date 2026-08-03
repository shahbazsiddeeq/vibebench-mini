import sqlite3
import re
from typing import Dict


def value_counts(db_path: str, table: str, column: str) -> Dict:
    """
    Returns a dict mapping each distinct value in the given column to its count.
    
    Args:
        db_path: Path to the SQLite database file
        table: Name of the table
        column: Name of the column
        
    Returns:
        Dictionary mapping distinct values to their counts
        
    Raises:
        ValueError: If table or column is an invalid identifier
    """
    # Validate table and column names as identifiers
    # SQLite identifiers must start with letter or underscore, contain only alphanumeric and underscores
    if not _is_valid_identifier(table):
        raise ValueError(f"Invalid table name: {table}")
    if not _is_valid_identifier(column):
        raise ValueError(f"Invalid column name: {column}")
    
    try:
        with sqlite3.connect(db_path) as conn:
            # Use parameterized query for safety, but identifiers must be in the query string
            # since SQL doesn't support parameterized identifiers
            query = f"SELECT {column}, COUNT(*) as count FROM {table} GROUP BY {column}"
            cursor = conn.execute(query)
            result = {}
            for row in cursor.fetchall():
                value, count = row
                result[value] = count
            return result
    except sqlite3.OperationalError as e:
        # If the table or column doesn't exist, raise ValueError
        raise ValueError(f"Database error: {str(e)}")


def _is_valid_identifier(name: str) -> bool:
    """
    Validates that a name is a valid SQLite identifier.
    
    Valid identifiers:
    - Start with a letter (a-z, A-Z) or underscore (_)
    - Contain only letters, digits (0-9), and underscores
    - Are not empty
    
    Args:
        name: The identifier to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not name:
        return False
    # Pattern: starts with letter or underscore, followed by letters, digits, or underscores
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    return bool(re.match(pattern, name))
