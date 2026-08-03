# src/solution.py

import sqlite3
import re

def paginate(db_path, table, page, page_size):
    # Validate inputs
    if not isinstance(db_path, str) or not isinstance(table, str):
        raise ValueError("Database path and table name must be strings.")
    
    if not isinstance(page, int) or not isinstance(page_size, int):
        raise ValueError("Page and page_size must be integers.")
    
    if page < 1 or page_size < 1:
        raise ValueError("Page and page_size must be greater than or equal to 1.")
    
    # Validate table name
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', table):
        raise ValueError("Invalid table name.")
    
    # Connect to the database and fetch the paginated results
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            offset = (page - 1) * page_size
            cursor.execute(f"SELECT * FROM {table} ORDER BY rowid LIMIT ? OFFSET ?", (page_size, offset))
            rows = cursor.fetchall()
            return [tuple(row) for row in rows]
    except sqlite3.Error as e:
        raise ValueError("Database error occurred.") from e
