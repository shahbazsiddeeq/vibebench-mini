import sqlite3
import re


def paginate(db_path, table, page, page_size):
    """
    Returns the rows for a 1-based page of an existing table.
    
    Args:
        db_path: Path to the SQLite database file
        table: Name of the table to paginate
        page: 1-based page number
        page_size: Number of rows per page
        
    Returns:
        List of tuples representing rows, ordered by rowid
        
    Raises:
        ValueError: If table name is invalid or page/page_size < 1
    """
    # Validate page and page_size
    if page < 1 or page_size < 1:
        raise ValueError("page and page_size must be >= 1")
    
    # Validate table name - must be a valid identifier
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', table):
        raise ValueError("Invalid table name")
    
    # Calculate offset
    offset = (page - 1) * page_size
    
    # Connect to database and fetch rows
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            f"SELECT * FROM {table} ORDER BY rowid LIMIT ? OFFSET ?",
            (page_size, offset)
        )
        rows = cursor.fetchall()
    
    # Convert to list of plain tuples
    return [tuple(row) for row in rows]
