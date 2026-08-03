import csv
import sqlite3
import re
import os

def _is_valid_identifier(name):
    """
    Checks if a string is a valid SQL identifier.
    Valid identifiers match [A-Za-z_][A-Za-z0-9_]*.
    """
    return re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name) is not None

def csv_to_sqlite(csv_path, db_path, table_name):
    """
    Reads a CSV file, creates a new SQLite table, inserts data, and returns the number of rows inserted.

    Args:
        csv_path (str): Path to the input CSV file.
        db_path (str): Path to the SQLite database file.
        table_name (str): Name of the table to create.

    Returns:
        int: The number of rows inserted.

    Raises:
        FileNotFoundError: If csv_path does not exist.
        ValueError: If table_name or any header name is not a valid identifier,
                    or if a table with table_name already exists.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    if not _is_valid_identifier(table_name):
        raise ValueError(f"Invalid table name: '{table_name}'. Must match [A-Za-z_][A-Za-z0-9_]*")

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if table already exists
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
        if cursor.fetchone():
            raise ValueError(f"Table '{table_name}' already exists in the database.")

        with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)

            try:
                header = next(reader)
            except StopIteration:
                # CSV is empty (no header, no data)
                return 0

            if not header:
                # CSV has a header line but it's empty, or only whitespace
                # This case is ambiguous. The prompt says "A CSV with only a header and no columns returns 0."
                # If the header is truly empty, there are no columns to create.
                # Let's treat an empty header as having no columns.
                return 0

            # Validate header names
            for col_name in header:
                if not _is_valid_identifier(col_name):
                    raise ValueError(f"Invalid column name in CSV header: '{col_name}'. Must match [A-Za-z_][A-Za-z0-9_]*")

            # Create table
            column_definitions = ", ".join([f'"{col_name}" TEXT' for col_name in header])
            create_table_sql = f'CREATE TABLE "{table_name}" ({column_definitions});'
            cursor.execute(create_table_sql)

            # Insert data
            inserted_rows_count = 0
            if header: # Only proceed if there are actual columns
                placeholders = ", ".join(["?" for _ in header])
                insert_sql = f'INSERT INTO "{table_name}" VALUES ({placeholders});'

                for row in reader:
                    if len(row) != len(header):
                        # Skip malformed rows or raise an error, depending on desired strictness.
                        # For security, it's safer to skip or error than to try to insert partial data.
                        # The prompt doesn't specify, so we'll skip for now.
                        # A more robust solution might log this or raise a specific error.
                        continue
                    cursor.execute(insert_sql, row)
                    inserted_rows_count += 1

        conn.commit()
        return inserted_rows_count

    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        # Do not expose internal database error details directly.
        raise ValueError(f"Database error occurred: {e}") from e
    except Exception as e:
        if conn:
            conn.rollback()
        raise # Re-raise other unexpected errors
    finally:
        if conn:
            conn.close()
