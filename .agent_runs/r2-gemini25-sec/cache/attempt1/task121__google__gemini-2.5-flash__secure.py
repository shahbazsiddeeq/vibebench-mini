import sqlite3
import re
import os

def paginate(db_path: str, table: str, page: int, page_size: int) -> list[tuple]:
    """
    Paginates rows from an SQLite table.

    Args:
        db_path: The path to the SQLite database file.
        table: The name of the table to paginate.
        page: The 1-based page number.
        page_size: The number of rows per page.

    Returns:
        A list of tuples, where each tuple represents a row.
        Returns an empty list if the page is past the end of the table.

    Raises:
        ValueError: If the table name is invalid or page/page_size < 1.
        sqlite3.Error: For database-related errors.
    """

    if not isinstance(db_path, str) or not db_path:
        raise ValueError("db_path must be a non-empty string.")
    if not os.path.exists(db_path):
        raise ValueError(f"Database file not found: {db_path}")
    if not os.path.isfile(db_path):
        raise ValueError(f"db_path is not a file: {db_path}")

    if not isinstance(table, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", table):
        raise ValueError("Invalid table name. Must be a valid SQL identifier.")

    if not isinstance(page, int) or page < 1:
        raise ValueError("Page number must be an integer greater than or equal to 1.")
    if not isinstance(page_size, int) or page_size < 1:
        raise ValueError("Page size must be an integer greater than or equal to 1.")

    offset = (page - 1) * page_size

    try:
        with sqlite3.connect(db_path) as conn:
            # Use a parameterized query for LIMIT and OFFSET, though SQLite
            # doesn't support parameters for these clauses directly.
            # However, for table name, we must validate it strictly as done above.
            # For LIMIT/OFFSET, since they are derived from validated integers,
            # direct insertion into the query string is safe here.
            query = f"SELECT * FROM {table} ORDER BY rowid LIMIT ? OFFSET ?"
            cursor = conn.execute(query, (page_size, offset))
            rows = cursor.fetchall()
            return rows
    except sqlite3.Error as e:
        # Re-raise database errors to avoid exposing internal details
        # while still indicating a problem.
        raise sqlite3.Error(f"Database error during pagination: {e}") from e
    except Exception as e:
        # Catch any other unexpected errors
        raise RuntimeError(f"An unexpected error occurred: {e}") from e
