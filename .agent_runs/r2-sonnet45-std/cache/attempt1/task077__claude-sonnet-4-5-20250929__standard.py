import csv
import re
import sqlite3
from pathlib import Path


def csv_to_sqlite(csv_path, db_path, table_name):
    """
    Import a CSV file into a SQLite database table.
    
    Args:
        csv_path: Path to the CSV file
        db_path: Path to the SQLite database
        table_name: Name of the table to create
        
    Returns:
        Number of rows inserted
        
    Raises:
        FileNotFoundError: If csv_path does not exist
        ValueError: If table_name or any header is invalid, or if table already exists
    """
    # Check if CSV file exists
    if not Path(csv_path).exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    # Validate table name
    if not _is_valid_identifier(table_name):
        raise ValueError(f"Invalid table name: {table_name}")
    
    # Read CSV file
    with open(csv_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        
        if headers is None:
            headers = []
        
        # Validate all header names
        for header in headers:
            if not _is_valid_identifier(header):
                raise ValueError(f"Invalid column name: {header}")
        
        # Read all rows into memory
        rows = list(reader)
    
    # Connect to database
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
        
        # Create table if there are headers
        if headers:
            columns_def = ', '.join(f'"{col}" TEXT' for col in headers)
            create_sql = f'CREATE TABLE "{table_name}" ({columns_def})'
            cursor.execute(create_sql)
            
            # Insert rows
            if rows:
                placeholders = ', '.join('?' * len(headers))
                insert_sql = f'INSERT INTO "{table_name}" ({", ".join(f\'"{h}\' for h in headers)}) VALUES ({placeholders})'
                
                for row in rows:
                    values = [row.get(h, '') for h in headers]
                    cursor.execute(insert_sql, values)
            
            conn.commit()
            return len(rows)
        else:
            # No headers, no table created, return 0
            return 0
    finally:
        conn.close()


def _is_valid_identifier(name):
    """
    Check if a name is a valid SQL identifier.
    Must match [A-Za-z_][A-Za-z0-9_]*
    """
    if not name:
        return False
    return re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name) is not None
