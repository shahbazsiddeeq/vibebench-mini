import csv
import re
import sqlite3
from pathlib import Path


def csv_to_sqlite(csv_path, db_path, table_name):
    """
    Reads a CSV file and imports it into a SQLite database.
    
    Args:
        csv_path: Path to the CSV file (first line is header)
        db_path: Path to the SQLite database file
        table_name: Name of the table to create
        
    Returns:
        Number of rows inserted
        
    Raises:
        FileNotFoundError: If csv_path does not exist
        ValueError: If table_name or any header name is invalid, or if table already exists
    """
    # Validate table name
    if not _is_valid_identifier(table_name):
        raise ValueError(f"Invalid table name: {table_name}")
    
    # Check if CSV file exists
    if not Path(csv_path).exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    # Read CSV file
    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            # Empty CSV file
            raise ValueError("CSV file is empty")
        
        # Validate all header names
        for header in headers:
            if not _is_valid_identifier(header):
                raise ValueError(f"Invalid column name: {header}")
        
        # Read all data rows
        data_rows = list(reader)
    
    # Connect to database and create table
    conn = sqlite3.connect(db_path)
    try:
        # Check if table already exists
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        )
        if cursor.fetchone() is not None:
            raise ValueError(f"Table '{table_name}' already exists")
        
        # Create table with all TEXT columns
        columns_def = ", ".join(f'"{header}" TEXT' for header in headers)
        create_sql = f'CREATE TABLE "{table_name}" ({columns_def})'
        cursor.execute(create_sql)
        
        # Insert data rows
        if data_rows:
            placeholders = ", ".join("?" * len(headers))
            quoted_headers = ", ".join(f'"{h}"' for h in headers)
            insert_sql = f'INSERT INTO "{table_name}" ({quoted_headers}) VALUES ({placeholders})'
            cursor.executemany(insert_sql, data_rows)
        
        conn.commit()
        return len(data_rows)
    
    finally:
        conn.close()


def _is_valid_identifier(name):
    """
    Check if a name is a valid SQL identifier matching [A-Za-z_][A-Za-z0-9_]*
    """
    if not name:
        return False
    return re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name) is not None
