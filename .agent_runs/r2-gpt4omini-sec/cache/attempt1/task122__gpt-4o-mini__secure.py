# src/solution.py

import sqlite3
import re

def _is_valid_identifier(identifier: str) -> bool:
    """Check if the identifier is a valid SQLite identifier."""
    return bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', identifier))

def value_counts(db_path: str, table: str, column: str) -> dict:
    """Return a dict mapping each distinct value in the given column to its count."""
    
    # Validate table and column identifiers
    if not _is_valid_identifier(table):
        raise ValueError(f"Invalid table name: {table}")
    if not _is_valid_identifier(column):
        raise ValueError(f"Invalid column name: {column}")

    # Connect to the SQLite database
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            query = f"SELECT {column}, COUNT(*) FROM {table} GROUP BY {column};"
            cursor.execute(query)
            rows = cursor.fetchall()
    except sqlite3.Error as e:
        raise ValueError("Database error occurred") from e

    # Construct the result dictionary
    result = {}
    for value, count in rows:
        result[value] = count

    return result
