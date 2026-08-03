import re
import sqlite3
from typing import Any


def bulk_update(conn: sqlite3.Connection, table: str, key_column: str, rows: list[dict]) -> int:
    """
    Apply bulk updates to a table within a single transaction.
    
    Args:
        conn: SQLite connection
        table: Table name (validated as identifier)
        key_column: Column name for WHERE clause (validated as identifier)
        rows: List of dicts with updates
        
    Returns:
        Total number of rows modified
        
    Raises:
        ValueError: If identifiers are invalid, rows is not a list, 
                   key_column is missing from a dict, or a dict has no other columns
    """
    # Validate rows is a list
    if not isinstance(rows, list):
        raise ValueError("rows must be a list")
    
    # Empty list returns 0
    if not rows:
        return 0
    
    # Validate identifiers
    identifier_pattern = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
    
    if not identifier_pattern.match(table):
        raise ValueError(f"Invalid table identifier: {table}")
    
    if not identifier_pattern.match(key_column):
        raise ValueError(f"Invalid key_column identifier: {key_column}")
    
    # Validate all column names in all rows
    all_columns = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("Each row must be a dict")
        all_columns.update(row.keys())
    
    for col in all_columns:
        if not identifier_pattern.match(col):
            raise ValueError(f"Invalid column identifier: {col}")
    
    # Validate each row has key_column and at least one other column
    for row in rows:
        if key_column not in row:
            raise ValueError(f"Row missing key_column '{key_column}'")
        
        # Check that there's at least one column other than key_column
        if len(row) < 2:
            raise ValueError(f"Row must have at least one column other than '{key_column}'")
    
    # Execute updates in a transaction
    total_modified = 0
    try:
        for row in rows:
            # Extract key value
            key_value = row[key_column]
            
            # Build SET clause from all columns except key_column
            set_columns = [col for col in row.keys() if col != key_column]
            
            # Build SQL: UPDATE table SET col1=?, col2=? WHERE key_column=?
            set_clause = ", ".join([f'"{col}"=?' for col in set_columns])
            sql = f'UPDATE "{table}" SET {set_clause} WHERE "{key_column}"=?'
            
            # Prepare values: SET values first, then key value
            values = [row[col] for col in set_columns] + [key_value]
            
            # Execute and accumulate row count
            cursor = conn.execute(sql, values)
            total_modified += cursor.rowcount
        
        # Commit the transaction
        conn.commit()
    except Exception:
        # Rollback on any error
        conn.rollback()
        raise
    
    return total_modified
