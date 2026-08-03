import csv
import os
import sqlite3
import re

def csv_to_sqlite(csv_path, db_path, table_name):
    # Check if the CSV file exists
    if not os.path.isfile(csv_path):
        raise FileNotFoundError(f"The file {csv_path} does not exist.")
    
    # Validate the table name
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', table_name):
        raise ValueError(f"Invalid table name: {table_name}")

    # Read the CSV file
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None)  # Get the header row

        # If there are no headers, return 0
        if headers is None or len(headers) == 0:
            return 0

        # Validate headers
        for header in headers:
            if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', header):
                raise ValueError(f"Invalid header name: {header}")

        # Connect to the SQLite database
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Check if the table already exists
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            if cursor.fetchone() is not None:
                raise ValueError(f"Table {table_name} already exists.")

            # Create the table with TEXT columns
            cursor.execute(f"CREATE TABLE \"{table_name}\" ({', '.join([f'\"{header}\" TEXT' for header in headers])});")

            # Insert the data rows
            rows = [tuple(row) for row in reader]
            cursor.executemany(f"INSERT INTO \"{table_name}\" ({', '.join([f'\"{header}\"' for header in headers])}) VALUES ({', '.join(['?' for _ in headers])});", rows)

            # Return the number of rows inserted
            return len(rows)
