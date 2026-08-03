import sqlite3
import re
from pathlib import Path


def create_table(db_path, table_name, columns):
    """
    Create a SQLite table from a column-name->type-string dict.
    
    Args:
        db_path: Path to the SQLite database file
        table_name: Name of the table to create
        columns: Dictionary mapping column names to type strings
        
    Raises:
        ValueError: If table_name or column names are invalid identifiers,
                   if type strings contain invalid characters,
                   if columns is empty,
                   or if a table with the same name already exists
    """
    
    # Validate that columns is not empty
    if not columns:
        raise ValueError("columns cannot be empty")
    
    # Validate table name
    if not _is_valid_identifier(table_name):
        raise ValueError(f"Invalid table name: {table_name}")
    
    # Validate column names and type strings
    for col_name, col_type in columns.items():
        if not _is_valid_identifier(col_name):
            raise ValueError(f"Invalid column name: {col_name}")
        if not _is_valid_type_string(col_type):
            raise ValueError(f"Invalid type string: {col_type}")
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        
        # Check if table already exists (case-insensitive)
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND LOWER(name)=LOWER(?)",
            (table_name,)
        )
        if cursor.fetchone() is not None:
            raise ValueError(f"Table {table_name} already exists")
        
        # Build the CREATE TABLE statement with quoted identifiers
        column_defs = []
        for col_name, col_type in columns.items():
            # Double-quote column names for safety
            column_defs.append(f'"{col_name}" {col_type}')
        
        # Double-quote table name for safety
        create_stmt = f'CREATE TABLE "{table_name}" ({", ".join(column_defs)})'
        
        # Execute the statement
        cursor.execute(create_stmt)
        conn.commit()
    finally:
        conn.close()


def _is_valid_identifier(name):
    """
    Check if a name matches the identifier pattern [A-Za-z_][A-Za-z0-9_]*
    
    Args:
        name: The identifier to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(name, str):
        return False
    pattern = r'^[A-Za-z_][A-Za-z0-9_]*$'
    return re.match(pattern, name) is not None


def _is_valid_type_string(type_str):
    """
    Check if a type string contains only letters, digits, underscores, spaces, and parentheses.
    
    Args:
        type_str: The type string to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(type_str, str):
        return False
    # Allow letters, digits, underscores, spaces, and parentheses
    pattern = r'^[A-Za-z0-9_\s()]+$'
    return re.match(pattern, type_str) is not None
