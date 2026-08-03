import sqlite3
import re


def bulk_update(conn: sqlite3.Connection, table: str, key_column: str, rows: list[dict]) -> int:
    """
    Bulk update rows in a table using a transaction.
    
    Args:
        conn: SQLite database connection
        table: Table name (validated identifier)
        key_column: Column name to use as key in WHERE clause (validated identifier)
        rows: List of dicts, each containing key_column and columns to update
        
    Returns:
        Total number of rows modified
        
    Raises:
        ValueError: If validation fails or rows structure is invalid
    """
    # Validate that rows is a list
    if not isinstance(rows, list):
        raise ValueError("rows must be a list")
    
    # Empty list returns 0
    if len(rows) == 0:
        return 0
    
    # Identifier validation pattern
    identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    
    def validate_identifier(name: str) -> None:
        """Validate an identifier against the allowed pattern."""
        if not identifier_pattern.match(name):
            raise ValueError(f"Invalid identifier: {name}")
    
    def quote_identifier(name: str) -> str:
        """Double-quote an identifier for SQL."""
        return f'"{name}"'
    
    # Validate table and key_column identifiers
    validate_identifier(table)
    validate_identifier(key_column)
    
    total_modified = 0
    
    # Start transaction
    conn.execute("BEGIN")
    
    try:
        for row_dict in rows:
            # Validate that key_column is present
            if key_column not in row_dict:
                raise ValueError(f"Row missing key column '{key_column}'")
            
            # Get columns to update (all except key_column)
            update_columns = {k: v for k, v in row_dict.items() if k != key_column}
            
            # Validate that there's at least one column to update
            if len(update_columns) == 0:
                raise ValueError("Row must contain at least one column to update besides key column")
            
            # Validate all column identifiers
            for col_name in update_columns.keys():
                validate_identifier(col_name)
            
            # Build the UPDATE statement
            set_clauses = [f"{quote_identifier(col)} = ?" for col in update_columns.keys()]
            set_clause = ", ".join(set_clauses)
            
            sql = f"UPDATE {quote_identifier(table)} SET {set_clause} WHERE {quote_identifier(key_column)} = ?"
            
            # Prepare values: update values followed by key value
            values = list(update_columns.values()) + [row_dict[key_column]]
            
            # Execute the update
            cursor = conn.execute(sql, values)
            total_modified += cursor.rowcount
        
        # Commit the transaction
        conn.commit()
        
    except Exception:
        # Rollback on any error
        conn.rollback()
        raise
    
    return total_modified
