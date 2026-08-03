import csv
import os
import sqlite3
import re
import secrets

def _is_valid_identifier(name):
    """Check if the provided name is a valid SQL identifier."""
    return bool(re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name))

def csv_to_sqlite(csv_path, db_path, table_name):
    """Import CSV data into an SQLite database table."""
    
    # Validate inputs
    if not os.path.isfile(csv_path):
        raise FileNotFoundError(f"The file {csv_path} does not exist.")
    
    if not _is_valid_identifier(table_name):
        raise ValueError(f"Invalid table name: {table_name}")
    
    # Read the CSV file
    with open(csv_path, mode='r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        headers = next(reader, None)  # Get the header row
        
        if headers is None or len(headers) == 0:
            return 0  # No columns to insert
        
        # Validate headers
        for header in headers:
            if not _is_valid_identifier(header):
                raise ValueError(f"Invalid header name: {header}")
        
        # Connect to the SQLite database
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Check if the table already exists
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            if cursor.fetchone() is not None:
                raise ValueError(f"Table {table_name} already exists.")
            
            # Create the table with TEXT columns
            cursor.execute(f"CREATE TABLE \"{table_name}\" ({', '.join(f'\"{header}\" TEXT' for header in headers)})")
            
            # Insert the data rows
            rows = [tuple(row) for row in reader]
            if rows:
                cursor.executemany(f"INSERT INTO \"{table_name}\" ({', '.join(f'\"{header}\"' for header in headers)}) VALUES ({', '.join('?' for _ in headers)})", rows)
            
            return len(rows)
