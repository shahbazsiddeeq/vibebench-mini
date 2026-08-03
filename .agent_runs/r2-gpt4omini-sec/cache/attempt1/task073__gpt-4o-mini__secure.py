import sqlite3
import re
import os

def validate_identifier(identifier):
    """Validate if the identifier matches the SQLite identifier pattern."""
    if not isinstance(identifier, str):
        raise ValueError("Identifier must be a string.")
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', identifier):
        raise ValueError(f"Invalid identifier: {identifier}")

def validate_type_string(type_string):
    """Validate if the type string contains only allowed characters."""
    if not isinstance(type_string, str):
        raise ValueError("Type string must be a string.")
    if not re.match(r'^[A-Za-z0-9_ ()]+$', type_string):
        raise ValueError(f"Invalid type string: {type_string}")

def create_table(db_path, table_name, columns):
    """Create a SQLite table with the specified name and columns."""
    # Validate inputs
    validate_identifier(table_name)
    
    if not isinstance(columns, dict) or not columns:
        raise ValueError("Columns must be a non-empty dictionary.")
    
    for column_name in columns:
        validate_identifier(column_name)
        validate_type_string(columns[column_name])
    
    # Check if the table already exists (case-insensitive)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = ?", (table_name,))
        if cursor.fetchone() is not None:
            raise ValueError(f"Table '{table_name}' already exists.")
    
    # Create the table
    column_definitions = ', '.join(f'"{col}" {typ}' for col, typ in columns.items())
    create_table_sql = f'CREATE TABLE "{table_name}" ({column_definitions})'
    
    with sqlite3.connect(db_path) as conn:
        conn.execute(create_table_sql)
