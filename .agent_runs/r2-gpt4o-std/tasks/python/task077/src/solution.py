import csv
import sqlite3
import re
from pathlib import Path

def csv_to_sqlite(csv_path, db_path, table_name):
    # Check if the table name is a valid identifier
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', table_name):
        raise ValueError(f"Invalid table name: {table_name}")

    # Check if the CSV file exists
    if not Path(csv_path).exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    # Read the CSV file
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None)

        # If there's no header, return 0
        if headers is None:
            return 0

        # Check if all headers are valid identifiers
        for header in headers:
            if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', header):
                raise ValueError(f"Invalid header name: {header}")

        # Connect to the SQLite database
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Check if the table already exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            if cursor.fetchone():
                raise ValueError(f"Table {table_name} already exists")

            # Create the table
            create_table_sql = f'CREATE TABLE "{table_name}" ({", ".join(f\'"{header}" TEXT\' for header in headers)})'
            cursor.execute(create_table_sql)

            # Prepare the insert statement
            insert_sql = f'INSERT INTO "{table_name}" ({", ".join(f\'"{header}"\' for header in headers)}) VALUES ({", ".join("?" for _ in headers)})'

            # Insert the data
            rows_inserted = 0
            for row in reader:
                cursor.execute(insert_sql, row)
                rows_inserted += 1

            return rows_inserted
