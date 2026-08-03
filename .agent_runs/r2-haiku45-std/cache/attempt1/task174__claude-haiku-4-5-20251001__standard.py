import sqlite3
import re


def bulk_update(conn: sqlite3.Connection, table: str, key_column: str, rows: list[dict]) -> int:
    """
    Apply bulk updates to a table within a single transaction.
    
    Args:
        conn: sqlite3 connection
        table: table name (validated as identifier)
        key_column: column name for WHERE clause (validated as identifier)
        rows: list of dicts, each containing key_column and at least one other column
    
    Returns:
        Total number of rows modified
    
    Raises:
        ValueError: if identifiers are invalid, rows is not a list, 
                   key_column is missing from a dict, or a dict has no columns to set
    """
    
    # Validate rows is a list
    if not isinstance(rows, list):
        raise ValueError("rows must be a list")
    
    # Empty list returns 0
    if not rows:
        return 0
    
    # Validate identifiers
    identifier_pattern = r'^[A-Za-z_][A-Za-z0-9_]*$'
    
    if not re.match(identifier_pattern, table):
        raise ValueError(f"Invalid table identifier: {table}")
    
    if not re.match(identifier_pattern, key_column):
        raise ValueError(f"Invalid key_column identifier: {key_column}")
    
    # Validate all column names in all rows
    all_columns = set()
    for row in rows:
        all_columns.update(row.keys())
    
    for col in all_columns:
        if not re.match(identifier_pattern, col):
            raise ValueError(f"Invalid column identifier: {col}")
    
    # Validate each row has key_column and at least one other column
    for row in rows:
        if key_column not in row:
            raise ValueError(f"Missing key_column '{key_column}' in row")
        if len(row) < 2:
            raise ValueError(f"Row must have at least one column to set besides key_column")
    
    # Build and execute updates in a transaction
    total_modified = 0
    
    try:
        for row in rows:
            # Extract key value
            key_value = row[key_column]
            
            # Get columns to set (all except key_column)
            set_columns = {k: v for k, v in row.items() if k != key_column}
            
            # Build SET clause with double-quoted identifiers
            set_clause = ", ".join(
                f'"{col}"=?' for col in set_columns.keys()
            )
            
            # Build WHERE clause with double-quoted identifier
            where_clause = f'"{key_column}"=?'
            
            # Build full SQL
            sql = f'UPDATE "{table}" SET {set_clause} WHERE {where_clause}'
            
            # Prepare values: SET values first, then key value
            values = list(set_columns.values()) + [key_value]
            
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
