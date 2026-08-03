import sqlite3
import re


def bulk_update(conn: sqlite3.Connection, table: str, key_column: str, rows: list[dict]) -> int:
    """
    Bulk update rows in a table using a transaction.
    
    Args:
        conn: SQLite database connection
        table: Table name (validated as identifier)
        key_column: Column name to use in WHERE clause (validated as identifier)
        rows: List of dicts, each containing key_column and columns to update
        
    Returns:
        Total number of rows modified
        
    Raises:
        ValueError: If validation fails or input is invalid
    """
    # Validate that rows is a list
    if not isinstance(rows, list):
        raise ValueError("rows must be a list")
    
    # Empty list returns 0
    if len(rows) == 0:
        return 0
    
    # Validate identifiers (table and key_column)
    identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    
    if not identifier_pattern.match(table):
        raise ValueError(f"Invalid table identifier: {table}")
    
    if not identifier_pattern.match(key_column):
        raise ValueError(f"Invalid key_column identifier: {key_column}")
    
    total_modified = 0
    
    try:
        # Start transaction
        conn.execute("BEGIN")
        
        for row_dict in rows:
            # Validate that row_dict is a dict
            if not isinstance(row_dict, dict):
                raise ValueError("Each row must be a dict")
            
            # Check that key_column exists in the dict
            if key_column not in row_dict:
                raise ValueError(f"Dict missing key_column: {key_column}")
            
            # Get columns to update (all except key_column)
            update_columns = {k: v for k, v in row_dict.items() if k != key_column}
            
            # Check that there's at least one column to update
            if len(update_columns) == 0:
                raise ValueError("Dict must contain at least one column to update besides key_column")
            
            # Validate all column identifiers
            for col in update_columns.keys():
                if not identifier_pattern.match(col):
                    raise ValueError(f"Invalid column identifier: {col}")
            
            # Build the UPDATE statement with quoted identifiers
            set_clauses = [f'"{col}" = ?' for col in update_columns.keys()]
            set_clause = ", ".join(set_clauses)
            
            sql = f'UPDATE "{table}" SET {set_clause} WHERE "{key_column}" = ?'
            
            # Prepare values: all update values followed by the key value
            values = list(update_columns.values()) + [row_dict[key_column]]
            
            # Execute the update
            cursor = conn.execute(sql, values)
            total_modified += cursor.rowcount
        
        # Commit transaction
        conn.commit()
        
    except Exception as e:
        # Rollback on any error
        conn.rollback()
        raise
    
    return total_modified
