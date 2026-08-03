import re
import sqlite3
import secrets

def _is_valid_identifier(name):
    """
    Checks if the given name is a valid SQL identifier.
    Valid identifiers match [A-Za-z_][A-Za-z0-9_]*.
    """
    return re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name) is not None

def upsert(db_path, table, record, key):
    """
    Inserts record into a SQLite table, or updates the existing row on a conflict
    of the key column.

    The key column must have a UNIQUE or PRIMARY KEY constraint.
    On conflict, every column in record other than key is overwritten with the new value,
    while columns not present in record are left unchanged.
    If record contains only the key, the existing row is left untouched.

    Args:
        db_path (str): Path to the SQLite database file.
        table (str): The name of the table.
        record (dict): A dictionary representing the row to insert or update.
        key (str): The name of the key column.

    Raises:
        ValueError: If table, key, or any record key is not a valid identifier.
        KeyError: If key is not present in record.
        RuntimeError: For unexpected database operation failures.
    """

    if not _is_valid_identifier(table):
        raise ValueError(f"Invalid table name: {table}")
    if not _is_valid_identifier(key):
        raise ValueError(f"Invalid key column name: {key}")
    if key not in record:
        raise KeyError(f"Key column '{key}' not found in record.")

    for col in record:
        if not _is_valid_identifier(col):
            raise ValueError(f"Invalid column name in record: {col}")

    quoted_table = f'"{table}"'
    quoted_key = f'"{key}"'

    columns = []
    placeholders = []
    values = []
    update_set_parts = []

    for col, value in record.items():
        quoted_col = f'"{col}"'
        columns.append(quoted_col)
        placeholders.append("?")
        values.append(value)
        if col != key:
            update_set_parts.append(f"{quoted_col} = EXCLUDED.{quoted_col}")

    insert_cols_str = ", ".join(columns)
    insert_placeholders_str = ", ".join(placeholders)

    # If only the key is present, no update should happen on conflict.
    # The ON CONFLICT clause should still be present to avoid an error,
    # but the DO UPDATE SET part should be omitted or effectively a no-op.
    if not update_set_parts:
        # If only the key is provided, we still need an ON CONFLICT clause
        # to prevent an INSERT error, but we don't want to update anything.
        # A common way to achieve a no-op update is to set a column to itself.
        # However, SQLite's UPSERT (ON CONFLICT DO UPDATE) requires at least one SET clause.
        # If we truly want to do nothing, we can use DO NOTHING.
        # The problem description says "if record contains only the key, the existing row is left untouched."
        # This implies DO NOTHING is the correct behavior.
        on_conflict_clause = f"ON CONFLICT {quoted_key} DO NOTHING"
    else:
        update_set_str = ", ".join(update_set_parts)
        on_conflict_clause = f"ON CONFLICT {quoted_key} DO UPDATE SET {update_set_str}"

    sql = f"""
        INSERT INTO {quoted_table} ({insert_cols_str})
        VALUES ({insert_placeholders_str})
        {on_conflict_clause};
    """

    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute(sql, values)
            conn.commit()
    except sqlite3.Error as e:
        # Do not expose internal database errors directly.
        # Log the error if a logging system is available.
        # For this task, re-raising a generic error or a specific custom error
        # is appropriate if the error is not due to invalid input.
        # Here, we assume input validation handles most user-induced errors.
        raise RuntimeError(f"Database operation failed: {e}") from e
