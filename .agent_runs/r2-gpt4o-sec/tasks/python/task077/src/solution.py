import csv
import sqlite3
import os
import re

def csv_to_sqlite(csv_path, db_path, table_name):
    # Validate table name
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', table_name):
        raise ValueError("Invalid table name")

    # Check if CSV file exists
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    # Read CSV file
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader, None)

        # Validate header
        if header is None:
            return 0
        for column_name in header:
            if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', column_name):
                raise ValueError(f"Invalid column name: {column_name}")

    # Connect to SQLite database
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Check if table already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if cursor.fetchone():
            raise ValueError(f"Table '{table_name}' already exists")

        # Create table
        create_table_sql = f'CREATE TABLE "{table_name}" ({", ".join(f\'"{name}" TEXT\' for name in header)})'
        cursor.execute(create_table_sql)

        # Insert data
        insert_sql = f'INSERT INTO "{table_name}" ({", ".join(f\'"{name}"\' for name in header)}) VALUES ({", ".join("?" for _ in header)})'
        rows_inserted = 0
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # Skip header
            for row in reader:
                cursor.execute(insert_sql, row)
                rows_inserted += 1

        return rows_inserted
