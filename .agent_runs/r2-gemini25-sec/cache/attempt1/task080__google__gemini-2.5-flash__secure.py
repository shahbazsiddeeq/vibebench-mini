import sqlite3
import collections

def batch_insert(db_path: str, table: str, rows: list[dict]) -> int:
    """
    Inserts all rows into the specified table in one transaction.
    Rolls back all changes on error. Raises RuntimeError on failure.

    Args:
        db_path: The path to the SQLite database file.
        table: The name of the table to insert into.
        rows: A list of dictionaries, where each dictionary represents a row
              and keys are column names.

    Returns:
        The number of rows successfully inserted.

    Raises:
        ValueError: If db_path, table, or rows are invalid.
        RuntimeError: If the insertion fails or data integrity issues are found.
    """
    if not isinstance(db_path, str) or not db_path:
        raise ValueError("db_path must be a non-empty string.")
    if not isinstance(table, str) or not table:
        raise ValueError("table must be a non-empty string.")
    if not isinstance(rows, list):
        raise ValueError("rows must be a list.")
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError("All items in 'rows' must be dictionaries.")

    if not rows:
        return 0

    # Validate table and column names to prevent SQL injection
    if not table.isidentifier():
        raise ValueError(f"Invalid table name: '{table}'. Table name must be a valid identifier.")

    # All rows must have the same keys for a batch insert
    first_row_keys = None
    if rows:
        first_row_keys = frozenset(rows[0].keys())
        for row in rows:
            if not isinstance(row, dict):
                raise ValueError("All items in 'rows' must be dictionaries.")
            current_row_keys = frozenset(row.keys())
            if current_row_keys != first_row_keys:
                raise RuntimeError("All rows must have the same keys for batch insertion.")
            for key in row.keys():
                if not isinstance(key, str) or not key.isidentifier():
                    raise ValueError(f"Invalid column name: '{key}'. Column names must be valid identifiers.")

    if not first_row_keys: # rows was not empty, but first_row_keys is empty, meaning first row was empty dict
        raise ValueError("Rows cannot contain empty dictionaries.")

    columns = list(first_row_keys)
    placeholders = ", ".join(["?"] * len(columns))
    column_names_sql = ", ".join(f'"{col}"' for col in columns) # Quote column names to handle potential keywords

    sql = f"INSERT INTO \"{table}\" ({column_names_sql}) VALUES ({placeholders})"

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            data_to_insert = []
            for row in rows:
                # Ensure the order of values matches the order of columns
                data_to_insert.append(tuple(row[col] for col in columns))

            cursor.executemany(sql, data_to_insert)
            conn.commit()
            return cursor.rowcount
    except sqlite3.Error as e:
        # Catch specific SQLite errors and re-raise as RuntimeError
        # Avoid exposing internal database error messages directly
        raise RuntimeError(f"Database operation failed: {e.__class__.__name__}") from e
    except Exception as e:
        # Catch any other unexpected errors
        raise RuntimeError(f"An unexpected error occurred during batch insert: {e.__class__.__name__}") from e
