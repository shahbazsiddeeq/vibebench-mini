import sqlite3
import re


def paginate(db_path, table, page, page_size):
    """
    Returns rows for a 1-based page of an existing table.
    
    Args:
        db_path: Path to the SQLite database file
        table: Table name (must be a valid identifier)
        page: Page number (1-based, must be >= 1)
        page_size: Number of rows per page (must be >= 1)
    
    Returns:
        List of tuples, where each tuple represents a row
    
    Raises:
        ValueError: If table name is invalid or page/page_size < 1
    """
    # Validate page and page_size
    if not isinstance(page, int) or page < 1:
        raise ValueError("page must be an integer >= 1")
    if not isinstance(page_size, int) or page_size < 1:
        raise ValueError("page_size must be an integer >= 1")
    
    # Validate table name - must be a valid identifier
    if not isinstance(table, str) or not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', table):
        raise ValueError("table name must be a valid identifier ([A-Za-z_][A-Za-z0-9_]*)")
    
    # Calculate offset
    offset = (page - 1) * page_size
    
    # Connect to database and fetch rows
    try:
        with sqlite3.connect(db_path) as conn:
            # Use parameterized query for LIMIT and OFFSET
            # Table name cannot be parameterized, but we've validated it above
            query = f"SELECT * FROM {table} ORDER BY rowid LIMIT ? OFFSET ?"
            cursor = conn.execute(query, (page_size, offset))
            rows = cursor.fetchall()
            
            # Ensure we return plain tuples (not sqlite3.Row objects)
            return [tuple(row) for row in rows]
    except sqlite3.Error as e:
        # Don't expose internal database errors
        raise ValueError(f"Database error occurred") from None
