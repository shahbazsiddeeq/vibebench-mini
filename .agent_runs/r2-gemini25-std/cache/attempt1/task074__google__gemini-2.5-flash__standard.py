import sqlite3
import re

def _is_valid_identifier(identifier):
    """Checks if the given string is a valid SQL identifier."""
    return re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", identifier) is not None

def upsert(db_path, table, record, key):
    """
    Inserts record into a SQLite table, or updates the existing row on a conflict of the key column.
    The key column must have a UNIQUE or PRIMARY KEY constraint.
    On conflict, every column in record other than key is overwritten with the new value,
    while columns not present in record are left unchanged.
    If record contains only the key, the existing row is left untouched.

    Args:
        db_path (str): Path to the SQLite database file.
        table (str): Name of the table.
        record (dict): Dictionary representing the row to insert/update.
        key (str): Name of the key column.

    Raises:
        ValueError: If table, key, or any record key is not a valid identifier.
        KeyError: If key is not in record.
    """
    if not _is_valid_identifier(table):
        raise ValueError(f"Invalid table name: {table}")
    if not _is_valid_identifier(key):
        raise ValueError(f"Invalid key column name: {key}")
    if key not in record:
        raise KeyError(f"Key '{key}' not found in record.")

    for col in record:
        if not _is_valid_identifier(col):
            raise ValueError(f"Invalid column name in record: {col}")

    columns = list(record.keys())
    values = list(record.values())

    # Double-quote identifiers for safety and to handle potential keywords
    quoted_table = f'"{table}"'
    quoted_key = f'"{key}"'
    quoted_columns = [f'"{col}"' for col in columns]

    # Build the INSERT statement
    insert_cols_str = ", ".join(quoted_columns)
    placeholders = ", ".join(["?"] * len(values))
    insert_sql = f"INSERT INTO {quoted_table} ({insert_cols_str}) VALUES ({placeholders})"

    # Build the ON CONFLICT DO UPDATE SET clause
    update_set_parts = []
    for col in columns:
        if col != key:
            update_set_parts.append(f'"{col}" = EXCLUDED."{col}"')

    if update_set_parts:
        on_conflict_clause = f"ON CONFLICT ({quoted_key}) DO UPDATE SET {', '.join(update_set_parts)}"
    else:
        # If only the key is present in the record, do nothing on conflict
        on_conflict_clause = f"ON CONFLICT ({quoted_key}) DO NOTHING"

    full_sql = f"{insert_sql} {on_conflict_clause};"

    with sqlite3.connect(db_path) as conn:
        conn.execute(full_sql, values)
        conn.commit()
