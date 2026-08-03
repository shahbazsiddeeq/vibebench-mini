import sqlite3
import re
import os

def value_counts(db_path: str, table: str, column: str) -> dict:
    """
    Returns a dict mapping each distinct value in the given column to its count,
    computed with GROUP BY.

    Raises ValueError if table or column is an invalid identifier.
    """
    if not isinstance(db_path, str) or not db_path:
        raise ValueError("db_path must be a non-empty string.")
    if not os.path.exists(db_path):
        raise ValueError(f"Database file not found: {db_path}")
    if not os.path.isfile(db_path):
        raise ValueError(f"db_path is not a file: {db_path}")

    # Validate table and column names to prevent SQL injection.
    # Valid identifiers typically consist of letters, numbers, and underscores,
    # and do not start with a number. SQLite allows more, but this is a safe subset.
    # We explicitly disallow common SQL injection characters.
    identifier_pattern = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")

    if not identifier_pattern.fullmatch(table):
        raise ValueError(f"Invalid table name: '{table}'")
    if not identifier_pattern.fullmatch(column):
        raise ValueError(f"Invalid column name: '{column}'")

    counts = {}
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # Use parameterized query for values, but table/column names must be
            # directly inserted after validation.
            query = f"SELECT {column}, COUNT(*) FROM {table} GROUP BY {column}"
            cursor.execute(query)
            for row in cursor.fetchall():
                # SQLite can return None for NULL values, which is fine for dict keys.
                value, count = row
                counts[value] = count
    except sqlite3.Error as e:
        # Catch specific SQLite errors and re-raise as a more generic error
        # to avoid exposing internal database details.
        raise RuntimeError(f"Database error occurred: {e}") from e
    except Exception as e:
        # Catch any other unexpected errors.
        raise RuntimeError(f"An unexpected error occurred: {e}") from e

    return counts
