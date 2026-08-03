import csv
import sqlite3
import re
from pathlib import Path

def csv_to_sqlite(csv_path, db_path, table_name):
    # Check if the CSV file exists
    if not Path(csv_path).exists():
        raise FileNotFoundError(f"CSV file {csv_path} does not exist.")

    # Validate table name
    if not is_valid_identifier(table_name):
        raise ValueError(f"Invalid table name: {table_name}")

    # Read the CSV file
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames

        # Validate headers
        if not headers or any(not is_valid_identifier(header) for header in headers):
            raise ValueError("Invalid header names in CSV.")

        # Connect to the SQLite database
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Check if the table already exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            if cursor.fetchone():
                raise ValueError(f"Table {table_name} already exists.")

            # Create table with all TEXT columns
            columns = ', '.join(f'"{header}" TEXT' for header in headers)
            create_table_sql = f'CREATE TABLE "{table_name}" ({columns})'
            cursor.execute(create_table_sql)

            # Insert data into the table
            insert_sql = f'INSERT INTO "{table_name}" ({", ".join(f\'"{header}"\' for header in headers)}) VALUES ({", ".join("?" for _ in headers)})'
            rows_inserted = 0
            for row in reader:
                cursor.execute(insert_sql, [row[header] for header in headers])
                rows_inserted += 1

            return rows_inserted

def is_valid_identifier(name):
    return re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name) is not None
