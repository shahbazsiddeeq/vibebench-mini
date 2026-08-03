import csv
import sqlite3
import re
import os


def _is_valid_identifier(name):
    """
    Checks if a string is a valid SQL identifier.
    Valid identifiers match [A-Za-z_][A-Za-z0-9_]*
    """
    return re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name) is not None


def csv_to_sqlite(csv_path, db_path, table_name):
    """
    Reads a CSV file, creates a new SQLite table, inserts data, and returns the number of rows inserted.

    Args:
        csv_path (str): Path to the CSV file.
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
        raise ValueError(f"Invalid table name: '{table_name}'")

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if table already exists
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if cursor.fetchone():
            raise ValueError(f"Table '{table_name}' already exists in the database.")

        with open(csv_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            try:
                header = next(reader)  # Read header row
            except StopIteration:
                # CSV is empty (no header, no data)
                return 0

            if not header:
                # CSV has a header row but it's empty, which is an invalid state for this task
                # as it implies no columns.
                # The problem statement implies a header with names.
                # If a CSV with only a header and no columns returns 0, this case is covered
                # by the subsequent check for `len(header) == 0`.
                pass

            for col_name in header:
                if not _is_valid_identifier(col_name):
                    raise ValueError(f"Invalid column name in CSV header: '{col_name}'")

            if not header:
                # If header is empty (e.g., CSV only has an empty first line), no columns to create.
                # Per "A CSV with only a header and no columns returns 0."
                return 0

            # Create table
            column_definitions = ", ".join([f'"{col_name}" TEXT' for col_name in header])
            create_table_sql = f'CREATE TABLE "{table_name}" ({column_definitions})'
            cursor.execute(create_table_sql)

            # Prepare for data insertion
            placeholders = ", ".join(["?" for _ in header])
            insert_sql = f'INSERT INTO "{table_name}" VALUES ({placeholders})'

            rows_inserted = 0
            for row in reader:
                if len(row) != len(header):
                    # Handle malformed rows (e.g., too many/few columns)
                    # For this task, we assume well-formed CSVs or skip malformed rows.
                    # The problem description doesn't specify error handling for malformed rows,
                    # so we'll insert what we can, padding with None if needed, or raising an error.
                    # For simplicity, let's assume rows match header length.
                    # If a row has fewer columns, sqlite3.execute will raise an error.
                    # If a row has more columns, sqlite3.execute will raise an error.
                    # So, we just pass the row as-is and let sqlite3 handle it.
                    pass
                cursor.execute(insert_sql, row)
                rows_inserted += 1

            conn.commit()
            return rows_inserted

    except sqlite3.Error as e:
        # Catch any SQLite specific errors during table creation or insertion
        conn.rollback() # Rollback any changes if an error occurred
        raise ValueError(f"Database error: {e}") from e
    finally:
        if conn:
            conn.close()
