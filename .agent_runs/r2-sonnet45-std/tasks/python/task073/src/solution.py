import sqlite3
import re


def create_table(db_path, table_name, columns):
    """
    Creates a SQLite table from a column-name->type-string dict.
    
    Args:
        db_path: Path to the SQLite database file
        table_name: Name of the table to create
        columns: Dictionary mapping column names to type strings
    
    Raises:
        ValueError: If validation fails or table already exists
    """
    # Validate columns is not empty
    if not columns:
        raise ValueError("columns dictionary cannot be empty")
    
    # Pattern for valid identifiers
    identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    
    # Pattern for valid type strings (letters, digits, underscores, spaces, parentheses)
    type_pattern = re.compile(r'^[A-Za-z0-9_ ()]+$')
    
    # Validate table name
    if not identifier_pattern.match(table_name):
        raise ValueError(f"Invalid table name: {table_name}")
    
    # Validate column names and type strings
    for col_name, col_type in columns.items():
        if not identifier_pattern.match(col_name):
            raise ValueError(f"Invalid column name: {col_name}")
        if not type_pattern.match(col_type):
            raise ValueError(f"Invalid type string: {col_type}")
    
    # Connect to database and check if table exists
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Check if table already exists (case-insensitive)
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND LOWER(name) = LOWER(?)",
            (table_name,)
        )
        if cursor.fetchone() is not None:
            raise ValueError(f"Table {table_name} already exists")
        
        # Build CREATE TABLE statement with quoted identifiers
        quoted_table_name = f'"{table_name}"'
        column_defs = []
        for col_name, col_type in columns.items():
            quoted_col_name = f'"{col_name}"'
            column_defs.append(f"{quoted_col_name} {col_type}")
        
        columns_str = ", ".join(column_defs)
        create_stmt = f"CREATE TABLE {quoted_table_name} ({columns_str})"
        
        cursor.execute(create_stmt)
        conn.commit()
