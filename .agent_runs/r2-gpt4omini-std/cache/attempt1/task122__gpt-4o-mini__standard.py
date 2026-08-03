import sqlite3
import re

def value_counts(db_path, table, column):
    # Validate table and column identifiers
    if not _is_valid_identifier(table) or not _is_valid_identifier(column):
        raise ValueError("Invalid table or column identifier")

    # Connect to the SQLite database
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Execute the query to count distinct values in the specified column
        cursor.execute(f"SELECT {column}, COUNT(*) FROM {table} GROUP BY {column}")
        rows = cursor.fetchall()

    # Convert the result into a dictionary
    return {row[0]: row[1] for row in rows}

def _is_valid_identifier(identifier):
    # Check if the identifier is a valid SQLite identifier
    return bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', identifier))
