import csv
import sqlite3
import re
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
    csv_file = Path(csv_path)
    if not csv_file.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    # Read CSV file
    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            # Empty CSV file
            raise ValueError("CSV file is empty")
        
        # Validate all header names
        if not header:
            raise ValueError("CSV file has no columns")
            
        for col_name in header:
            if not _is_valid_identifier(col_name):
                raise ValueError(f"Invalid column name: {col_name}")
        
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
        # Use double quotes for identifiers as specified
        columns_def = ', '.join(f'"{col}" TEXT' for col in header)
        create_sql = f'CREATE TABLE "{table_name}" ({columns_def})'
        cursor.execute(create_sql)
        
        # Insert data rows
        rows_inserted = 0
        if data_rows:
            placeholders = ', '.join('?' * len(header))
            insert_sql = f'INSERT INTO "{table_name}" VALUES ({placeholders})'
            
            for row in data_rows:
                # Pad row with None if it has fewer columns than header
                # Truncate if it has more columns
                padded_row = row[:len(header)]
                while len(padded_row) < len(header):
                    padded_row.append('')
                
                cursor.execute(insert_sql, padded_row)
                rows_inserted += 1
        
        conn.commit()
        return rows_inserted
        
    finally:
        conn.close()


def _is_valid_identifier(name):
    """
    Check if a name is a valid SQL identifier matching [A-Za-z_][A-Za-z0-9_]*
    
    Args:
        name: String to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not name:
        return False
    pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    return pattern.match(name) is not None
