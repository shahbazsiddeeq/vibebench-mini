import sqlite3
import re

def paginate(db_path, table, page, page_size):
    """
    Returns the rows for a 1-based page of an existing table, ordered by rowid,
    using LIMIT/OFFSET. Each row is returned as a plain tuple of its column values
    in table (SELECT *) order, and the result is a list of such tuples (empty list
    when the page is past the end).

    Args:
        db_path (str): The path to the SQLite database file.
        table (str): The name of the table.
        page (int): The 1-based page number.
        page_size (int): The number of rows per page.

    Returns:
        list: A list of tuples, where each tuple represents a row.

    Raises:
        ValueError: For an invalid table name or page/page_size < 1.
    """
    if not isinstance(table, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", table):
        raise ValueError("Invalid table name.")
    if page < 1:
        raise ValueError("Page number must be 1 or greater.")
    if page_size < 1:
        raise ValueError("Page size must be 1 or greater.")

    offset = (page - 1) * page_size

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Using f-string for table name is safe here because it's already validated
        query = f"SELECT * FROM {table} ORDER BY rowid LIMIT ? OFFSET ?"
        cursor.execute(query, (page_size, offset))
        rows = cursor.fetchall()
    return rows
