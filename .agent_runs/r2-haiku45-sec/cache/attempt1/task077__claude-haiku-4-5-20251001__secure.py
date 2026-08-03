import csv
import sqlite3
import re
from pathlib import Path


def _is_valid_identifier(name: str) -> bool:
    """Check if name is a valid SQL identifier matching [A-Za-z_][A-Za-z0-9_]*"""
    return bool(re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name))


def csv_to_sqlite(csv_path: str, db_path: str, table_name: str) -> int:
    """
    Read a CSV file and import it into a SQLite database.
    
    Args:
        csv_path: Path to the CSV file (must exist)
        db_path: Path to the SQLite database file
        table_name: Name of the table to create (must be a valid identifier)
    
    Returns:
        Number of rows inserted
    
    Raises:
        FileNotFoundError: If csv_path does not exist
        ValueError: If table_name or any header is not a valid identifier,
                   or if the table already exists
    """
    # Validate table_name
    if not _is_valid_identifier(table_name):
        raise ValueError(f"Invalid table name: {table_name}")
    
    # Check if CSV file exists
    csv_file = Path(csv_path)
    if not csv_file.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    # Read CSV and extract header
    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError("CSV file is empty")
    
    if not header:
        raise ValueError("CSV file has no columns")
    
    # Validate all header names
    for col_name in header:
        if not _is_valid_identifier(col_name):
            raise ValueError(f"Invalid column name: {col_name}")
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        
        # Check if table already exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        )
        if cursor.fetchone() is not None:
            raise ValueError(f"Table already exists: {table_name}")
        
        # Create table with all TEXT columns
        # Use double quotes for identifiers as per spec
        col_defs = ', '.join(f'"{col}" TEXT' for col in header)
        create_sql = f'CREATE TABLE "{table_name}" ({col_defs})'
        cursor.execute(create_sql)
        
        # Insert data rows
        placeholders = ', '.join('?' * len(header))
        insert_sql = f'INSERT INTO "{table_name}" ({", ".join(f\'"{col}\' for col in header)}) VALUES ({placeholders})'
        
        row_count = 0
        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Extract values in header order
                values = [row.get(col, '') for col in header]
                cursor.execute(insert_sql, values)
                row_count += 1
        
        conn.commit()
        return row_count
    
    finally:
        conn.close()
