import csv
import sqlite3
import re
from pathlib import Path

def is_valid_identifier(name):
    return re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name) is not None

def csv_to_sqlite(csv_path, db_path, table_name):
    # Validate table name
    if not is_valid_identifier(table_name):
        raise ValueError(f"Invalid table name: {table_name}")

    # Check if CSV file exists
    csv_file = Path(csv_path)
    if not csv_file.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    # Read CSV header and data
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader, None)
        if header is None:
            return 0  # No data to insert

        # Validate header names
        for column_name in header:
            if not is_valid_identifier(column_name):
                raise ValueError(f"Invalid column name: {column_name}")

        # Connect to SQLite database
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Check if table already exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            if cursor.fetchone() is not None:
                raise ValueError(f"Table '{table_name}' already exists")

            # Create table with TEXT columns
            columns = ', '.join(f'"{name}" TEXT' for name in header)
            create_table_sql = f'CREATE TABLE "{table_name}" ({columns})'
            cursor.execute(create_table_sql)

            # Insert data rows
            insert_sql = f'INSERT INTO "{table_name}" ({", ".join(f\'"{name}"\' for name in header)}) VALUES ({", ".join("?" for _ in header)})'
            rows_inserted = 0
            for row in reader:
                cursor.execute(insert_sql, row)
                rows_inserted += 1

            return rows_inserted
