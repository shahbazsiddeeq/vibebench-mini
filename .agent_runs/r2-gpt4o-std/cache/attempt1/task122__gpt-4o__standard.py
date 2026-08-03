# src/solution.py

import sqlite3
import re

def value_counts(db_path, table, column):
    # Validate table and column names
    if not _is_valid_identifier(table) or not _is_valid_identifier(column):
        raise ValueError("Invalid table or column name")

    query = f"SELECT {column}, COUNT(*) FROM {table} GROUP BY {column}"
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
    
    return {row[0]: row[1] for row in result}

def _is_valid_identifier(name):
    # SQLite identifiers must start with a letter or underscore and can contain letters, digits, and underscores
    return re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name) is not None
