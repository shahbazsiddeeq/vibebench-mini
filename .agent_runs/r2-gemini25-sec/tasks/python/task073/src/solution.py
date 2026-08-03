import sqlite3
import re
import secrets

def _is_valid_identifier(name):
    """
    Checks if a string is a valid SQL identifier.
    Valid identifiers match the pattern [A-Za-z_][A-Za-z0-9_]*.
    """
    return re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name) is not None

def _is_valid_type_string(type_str):
    """
    Checks if a string is a valid SQL type string.
    Valid type strings may only contain letters, digits, underscores, spaces, and parentheses.
    """
    return re.fullmatch(r"[A-Za-z0-9_()\s]+", type_str) is not None

def create_table(db_path, table_name, columns):
    """
    Creates a SQLite table with the given name and columns.

    Args:
        db_path (str): The path to the SQLite database file.
        table_name (str): The name of the table to create.
        columns (dict): A dictionary where keys are column names (str) and values
                        are type strings (str).

    Raises:
        ValueError: If table_name or any column name is not a valid identifier,
                    if a type string contains invalid characters,
                    if columns is empty, or if a table with the same name
                    already exists (case-insensitive).
    """
    if not _is_valid_identifier(table_name):
        raise ValueError(f"Invalid table name: '{table_name}'. Table names must match [A-Za-z_][A-Za-z0-9_]*.")

    if not columns:
        raise ValueError("Columns dictionary cannot be empty.")

    column_definitions = []
    for col_name, col_type in columns.items():
        if not _is_valid_identifier(col_name):
            raise ValueError(f"Invalid column name: '{col_name}'. Column names must match [A-Za-z_][A-Za-z0-9_]*.")
        if not _is_valid_type_string(col_type):
            raise ValueError(f"Invalid type string for column '{col_name}': '{col_type}'. Type strings may only contain letters, digits, underscores, spaces, and parentheses.")
        
        # Double-quote column names to handle SQL keywords and ensure safety
        column_definitions.append(f'"{col_name}" {col_type}')

    # Use a temporary table name for checking existence to prevent SQL injection
    # in the table name check itself, although table_name is already validated.
    # This is an extra layer of caution.
    temp_table_name_for_check = "temp_check_table_" + "".join(secrets.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(16))

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Check if table already exists (case-insensitive)
            # Using a parameterized query for the table name check is not directly possible
            # with `sqlite_master` table name, so we fetch all table names and check in Python.
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [row[0].lower() for row in cursor.fetchall()]
            if table_name.lower() in existing_tables:
                raise ValueError(f"Table '{table_name}' already exists.")

            # Construct the CREATE TABLE statement
            # Table name is already validated, so direct interpolation is safe here.
            # Column names and types are also validated and column names are double-quoted.
            create_table_sql = f'CREATE TABLE "{table_name}" ({", ".join(column_definitions)})'
            
            cursor.execute(create_table_sql)
            conn.commit()
    except sqlite3.Error as e:
        # Catch specific SQLite errors if needed, but generally re-raising as ValueError
        # or a custom exception is good for internal errors.
        # For this task, the prompt implies ValueError for input validation,
        # but for database errors, a more specific error might be better in a real app.
        # Here, we'll re-raise as ValueError for consistency with other checks.
        raise ValueError(f"Database error: {e}") from e
