import sqlite3
import re

def _is_valid_identifier(name):
    """Checks if a name is a valid SQL identifier pattern [A-Za-z_][A-Za-z0-9_]*."""
    return re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name) is not None

def create_table(db_path, table_name, columns):
    """
    Creates a SQLite table from a column-name->type-string dict.

    Table and column names must match the identifier pattern [A-Za-z_][A-Za-z0-9_]*
    and are double-quoted when interpolated; type strings may only contain letters,
    digits, underscores, spaces and parentheses (e.g. "INTEGER PRIMARY KEY", "VARCHAR(255)").

    Raises ValueError if table_name or any column name is not a valid identifier,
    if a type string contains other characters, if columns is empty, or if a table
    with the same name already exists (comparison is case-insensitive, matching
    SQLite semantics).
    """
    if not _is_valid_identifier(table_name):
        raise ValueError(f"Invalid table name: '{table_name}'")

    if not columns:
        raise ValueError("Columns dictionary cannot be empty.")

    column_definitions = []
    for col_name, col_type in columns.items():
        if not _is_valid_identifier(col_name):
            raise ValueError(f"Invalid column name: '{col_name}'")
        # Type strings may only contain letters, digits, underscores, spaces and parentheses
        if not re.fullmatch(r"[A-Za-z0-9_()\s]+", col_type):
            raise ValueError(f"Invalid characters in column type for '{col_name}': '{col_type}'")
        column_definitions.append(f'"{col_name}" {col_type}')

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if table already exists (case-insensitive)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE ?", (table_name,))
        if cursor.fetchone():
            raise ValueError(f"Table '{table_name}' already exists.")

        columns_sql = ", ".join(column_definitions)
        create_table_sql = f'CREATE TABLE "{table_name}" ({columns_sql});'
        cursor.execute(create_table_sql)
        conn.commit()
    finally:
        if conn:
            conn.close()
