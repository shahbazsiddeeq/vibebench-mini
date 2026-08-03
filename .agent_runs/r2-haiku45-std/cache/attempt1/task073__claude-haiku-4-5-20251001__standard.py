import sqlite3
import re


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
    
    # Validate identifier pattern: [A-Za-z_][A-Za-z0-9_]*
    identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    
    # Validate table_name
    if not identifier_pattern.match(table_name):
        raise ValueError(f"Invalid table name: {table_name}")
    
    # Validate column names
    for col_name in columns.keys():
        if not identifier_pattern.match(col_name):
            raise ValueError(f"Invalid column name: {col_name}")
    
    # Validate type strings: only letters, digits, underscores, spaces, and parentheses
    type_pattern = re.compile(r'^[A-Za-z0-9_\s()]+$')
    for col_type in columns.values():
        if not type_pattern.match(col_type):
            raise ValueError(f"Invalid type string: {col_type}")
    
    # Connect to database
    with sqlite3.connect(db_path) as conn:
        # Check if table already exists (case-insensitive)
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND LOWER(name)=LOWER(?)",
            (table_name,)
        )
        if cursor.fetchone() is not None:
            raise ValueError(f"Table {table_name} already exists")
        
        # Build the CREATE TABLE statement with quoted identifiers
        col_defs = []
        for col_name, col_type in columns.items():
            col_defs.append(f'"{col_name}" {col_type}')
        
        create_stmt = f'CREATE TABLE "{table_name}" ({", ".join(col_defs)})'
        
        # Execute the CREATE TABLE statement
        conn.execute(create_stmt)
        conn.commit()
