import csv
import sqlite3
import re
from pathlib import Path


def csv_to_sqlite(csv_path, db_path, table_name):
    """
    Reads a CSV file and imports it into a SQLite database.
    
    Args:
        csv_path: Path to the CSV file
        db_path: Path to the SQLite database file
        table_name: Name of the table to create
        
    Returns:
        Number of rows inserted
        
    Raises:
        FileNotFoundError: If csv_path does not exist
        ValueError: If table_name or any header is not a valid identifier,
                   or if the table already exists
    """
    # Check if CSV file exists
    if not Path(csv_path).exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    # Validate identifier pattern
    identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    
    def is_valid_identifier(name):
        return identifier_pattern.match(name) is not None
    
    # Validate table name
    if not is_valid_identifier(table_name):
        raise ValueError(f"Invalid table name: {table_name}")
    
    # Read CSV and get headers
    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
    
    # Validate all headers
    for header in headers:
        if not is_valid_identifier(header):
            raise ValueError(f"Invalid column name: {header}")
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if table already exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        )
        if cursor.fetchone() is not None:
            raise ValueError(f"Table already exists: {table_name}")
        
        # Create table with all TEXT columns
        quoted_headers = [f'"{h}"' for h in headers]
        column_defs = ', '.join([f'{h} TEXT' for h in quoted_headers])
        create_sql = f'CREATE TABLE "{table_name}" ({column_defs})'
        cursor.execute(create_sql)
        
        # Insert rows
        if rows:
            placeholders = ', '.join(['?' for _ in headers])
            insert_sql = f'INSERT INTO "{table_name}" ({", ".join(quoted_headers)}) VALUES ({placeholders})'
            cursor.executemany(insert_sql, rows)
        
        conn.commit()
        return len(rows)
    finally:
        conn.close()
