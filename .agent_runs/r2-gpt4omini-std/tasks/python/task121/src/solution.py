import sqlite3
import re

def paginate(db_path, table, page, page_size):
    # Validate table name
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', table):
        raise ValueError("Invalid table name")
    
    # Validate page and page_size
    if page < 1 or page_size < 1:
        raise ValueError("Page and page_size must be greater than 0")
    
    # Calculate offset
    offset = (page - 1) * page_size
    
    # Connect to the database and fetch the paginated rows
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table} ORDER BY rowid LIMIT ? OFFSET ?", (page_size, offset))
        rows = cursor.fetchall()
    
    return rows
