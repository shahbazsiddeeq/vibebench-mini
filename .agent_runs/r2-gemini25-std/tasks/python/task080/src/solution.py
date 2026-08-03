import sqlite3

def batch_insert(db_path, table, rows):
    """
    Inserts all rows into the specified table in one transaction.
    Rolls back all changes on error. Raises RuntimeError on failure.

    Args:
        db_path (str): Path to the SQLite database file.
        table (str): Name of the table to insert into.
        rows (list): A list of dictionaries, where each dictionary represents a row.
                     Keys are column names and values are the data to insert.

    Returns:
        int: The number of rows successfully inserted.

    Raises:
        RuntimeError: If any error occurs during the transaction, including
                      database errors or inconsistent row structures.
        ValueError: If column names contain characters that could lead to SQL injection.
    """
    if not rows:
        return 0

    # Validate column names for potential SQL injection
    for row in rows:
        for col_name in row.keys():
            if not col_name.replace('_', '').isalnum():
                raise ValueError(f"Invalid column name '{col_name}'. Column names must be alphanumeric or contain underscores.")

    first_row_keys = list(rows[0].keys())
    if not first_row_keys:
        raise RuntimeError("Cannot insert empty rows.")

    # Check for consistent keys across all rows
    for i, row in enumerate(rows):
        if list(row.keys()) != first_row_keys:
            raise RuntimeError(f"Inconsistent keys found in row {i}: expected {first_row_keys}, got {list(row.keys())}")

    columns = ", ".join(first_row_keys)
    placeholders = ", ".join(["?"] * len(first_row_keys))
    insert_sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            data_to_insert = [tuple(row[key] for key in first_row_keys) for row in rows]
            cursor.executemany(insert_sql, data_to_insert)
            conn.commit()
            return cursor.rowcount
    except sqlite3.Error as e:
        raise RuntimeError(f"Database error during batch insert: {e}")
    except Exception as e:
        # Catch any other unexpected errors
        raise RuntimeError(f"An unexpected error occurred: {e}")
