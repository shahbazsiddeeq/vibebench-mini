import sqlite3
import re

def create_table(db_path, table_name, columns):
    # Validate table name
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', table_name):
        raise ValueError(f"Invalid table name: {table_name}")

    # Validate columns
    if not columns or not isinstance(columns, dict):
        raise ValueError("Columns must be a non-empty dictionary.")
    
    for column_name in columns:
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', column_name):
            raise ValueError(f"Invalid column name: {column_name}")
        if not re.match(r'^[A-Za-z0-9_ ()]+$', columns[column_name]):
            raise ValueError(f"Invalid type string for column {column_name}: {columns[column_name]}")

    # Connect to the database
    with sqlite3.connect(db_path) as conn:
        # Check if the table already exists (case-insensitive)
        existing_tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        existing_table_names = {table[0].lower() for table in existing_tables}
        
        if table_name.lower() in existing_table_names:
            raise ValueError(f"Table {table_name} already exists.")

        # Create the table
        columns_definition = ', '.join(f'"{col}" {col_type}' for col, col_type in columns.items())
        create_table_sql = f'CREATE TABLE "{table_name}" ({columns_definition})'
        conn.execute(create_table_sql)
