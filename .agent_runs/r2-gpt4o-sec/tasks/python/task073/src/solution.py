import sqlite3
import re
from typing import Dict

def create_table(db_path: str, table_name: str, columns: Dict[str, str]) -> None:
    # Regular expressions for validation
    identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    type_pattern = re.compile(r'^[A-Za-z0-9_ ()]+$')

    # Validate table name
    if not identifier_pattern.match(table_name):
        raise ValueError("Invalid table name")

    # Validate columns
    if not columns:
        raise ValueError("Columns dictionary cannot be empty")

    for column_name, column_type in columns.items():
        if not identifier_pattern.match(column_name):
            raise ValueError(f"Invalid column name: {column_name}")
        if not type_pattern.match(column_type):
            raise ValueError(f"Invalid type string: {column_type}")

    # Connect to the database
    with sqlite3.connect(db_path) as conn:
        # Check if table already exists (case-insensitive)
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND lower(name) = ?",
            (table_name.lower(),)
        )
        if cursor.fetchone():
            raise ValueError(f"Table '{table_name}' already exists")

        # Create table SQL statement
        columns_def = ", ".join(
            f'"{name}" {type_}' for name, type_ in columns.items()
        )
        create_table_sql = f'CREATE TABLE "{table_name}" ({columns_def})'

        # Execute the SQL statement
        conn.execute(create_table_sql)
