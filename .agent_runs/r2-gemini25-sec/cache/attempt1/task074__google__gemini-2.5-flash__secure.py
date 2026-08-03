import sqlite3
import re

def _is_valid_identifier(name: str) -> bool:
    """
    Checks if the given string is a valid SQL identifier.
    Valid identifiers match [A-Za-z_][A-Za-z0-9_]*.
    """
    return bool(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name))

def upsert(db_path: str, table: str, record: dict, key: str):
    """
    Inserts record into a SQLite table, or updates the existing row on a conflict
    of the key column.

    The key column must have a UNIQUE or PRIMARY KEY constraint.
    On conflict, every column in record other than key is overwritten with the
    new value, while columns not present in record are left unchanged; if record
    contains only the key, the existing row is left untouched.

    table, key, and all record keys must be valid identifiers matching
    [A-Za-z_][A-Za-z0-9_]*, are double-quoted when interpolated, and a value
    that is not a valid identifier raises ValueError. Values are always passed
    as bound parameters.

    Raises KeyError if key is not in record.
    """
    if not _is_valid_identifier(table):
        raise ValueError(f"Invalid table name: {table}")
    if not _is_valid_identifier(key):
        raise ValueError(f"Invalid key column name: {key}")

    if key not in record:
        raise KeyError(f"Key column '{key}' not found in record.")

    for col_name in record.keys():
        if not _is_valid_identifier(col_name):
            raise ValueError(f"Invalid column name in record: {col_name}")

    # Double-quote identifiers for safety and to handle potential keywords
    quoted_table = f'"{table}"'
    quoted_key = f'"{key}"'

    columns = []
    placeholders = []
    values = []
    update_set_clauses = []

    for col, value in record.items():
        quoted_col = f'"{col}"'
        columns.append(quoted_col)
        placeholders.append("?")
        values.append(value)
        if col != key:
            update_set_clauses.append(f"{quoted_col} = EXCLUDED.{quoted_col}")

    insert_cols_str = ", ".join(columns)
    insert_placeholders_str = ", ".join(placeholders)

    if not update_set_clauses:
        # If only the key is present in the record, we don't want to update anything.
        # The ON CONFLICT DO NOTHING clause handles this by preventing an update
        # if there's a conflict and no other columns to change.
        # However, if there are no other columns, we still need a valid DO clause.
        # DO NOTHING is the correct behavior here.
        on_conflict_clause = f"ON CONFLICT {quoted_key} DO NOTHING"
    else:
        update_set_str = ", ".join(update_set_clauses)
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
