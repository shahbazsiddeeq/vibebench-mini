import sqlite3
import re


def paginate(db_path, table, page, page_size):
    """
    Returns rows for a 1-based page of an existing table.
    
    Args:
        db_path: Path to the SQLite database
        table: Table name (must be valid identifier)
        page: Page number (1-based, must be >= 1)
        page_size: Number of rows per page (must be >= 1)
    
    Returns:
        List of tuples, where each tuple represents a row
    
    Raises:
        ValueError: If table name is invalid or page/page_size < 1
    """
    # Validate page and page_size
    if page < 1:
        raise ValueError("page must be >= 1")
    if page_size < 1:
        raise ValueError("page_size must be >= 1")
    
    # Validate table name
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', table):
        raise ValueError("Invalid table name")
    
    # Calculate offset
    offset = (page - 1) * page_size
    
    # Query the database
    with sqlite3.connect(db_path) as conn:
        # Use parameterized query for LIMIT and OFFSET, but table name must be inserted directly
        # since it can't be parameterized
        query = f"SELECT * FROM {table} ORDER BY rowid LIMIT ? OFFSET ?"
        cursor = conn.execute(query, (page_size, offset))
        rows = cursor.fetchall()
    
    # Ensure we return plain tuples (not Row objects)
    return [tuple(row) for row in rows]
