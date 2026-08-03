import sqlite3
import re
from typing import List, Tuple


def paginate(db_path: str, table: str, page: int, page_size: int) -> List[Tuple]:
    """
    Retrieve paginated rows from a SQLite table.
    
    Args:
        db_path: Path to the SQLite database file
        table: Name of the table to query (must be a valid identifier)
        page: 1-based page number (must be >= 1)
        page_size: Number of rows per page (must be >= 1)
    
    Returns:
        List of tuples representing rows, ordered by rowid
    
    Raises:
        ValueError: If table name is invalid or page/page_size < 1
    """
    # Validate page and page_size
    if page < 1:
        raise ValueError("page must be >= 1")
    if page_size < 1:
        raise ValueError("page_size must be >= 1")
    
    # Validate table name - must be a valid identifier [A-Za-z_][A-Za-z0-9_]*
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', table):
        raise ValueError(f"Invalid table name: {table}")
    
    # Calculate offset
    offset = (page - 1) * page_size
    
    # Connect to database and fetch rows
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Use parameterized query for LIMIT and OFFSET values
        # Table name cannot be parameterized, but we've validated it
        query = f"SELECT * FROM {table} ORDER BY rowid LIMIT ? OFFSET ?"
        cursor.execute(query, (page_size, offset))
        rows = cursor.fetchall()
    
    # Convert to list of tuples (fetchall already returns tuples)
    return [tuple(row) for row in rows]
