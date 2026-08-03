import sqlite3
import re
from typing import List, Dict, Any


def batch_insert(db_path: str, table: str, rows: List[Dict[str, Any]]) -> int:
    """
    Insert all rows into the specified table in a single transaction.
    
    Args:
        db_path: Path to the SQLite database file
        table: Name of the table to insert into
        rows: List of dictionaries representing rows to insert
    
    Returns:
        Number of rows inserted
    
    Raises:
        RuntimeError: On database errors or mismatched row keys
        ValueError: On invalid column names (potential SQL injection)
    """
    if not rows:
        return 0
    
    # Validate table name to prevent SQL injection
    if not _is_valid_identifier(table):
        raise ValueError("Invalid table name")
    
    # Get column names from first row
    columns = list(rows[0].keys())
    
    # Validate all column names
    for col in columns:
        if not _is_valid_identifier(col):
            raise ValueError(f"Invalid column name: {col}")
    
    # Verify all rows have the same keys
    for i, row in enumerate(rows):
        if set(row.keys()) != set(columns):
            raise RuntimeError(f"Row {i} has mismatched keys")
    
    try:
        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.cursor()
            
            # Build parameterized INSERT statement
            placeholders = ', '.join(['?' for _ in columns])
            column_list = ', '.join(columns)
            sql = f"INSERT INTO {table} ({column_list}) VALUES ({placeholders})"
            
            # Insert all rows
            for row in rows:
                # Ensure values are in the same order as columns
                values = [row[col] for col in columns]
                cursor.execute(sql, values)
            
            # Commit transaction
            conn.commit()
            count = len(rows)
            
            return count
            
        except Exception as e:
            # Rollback on any error
            conn.rollback()
            raise RuntimeError(f"Database operation failed: {str(e)}")
        finally:
            conn.close()
            
    except sqlite3.Error as e:
        raise RuntimeError(f"Database connection failed: {str(e)}")


def _is_valid_identifier(name: str) -> bool:
    """
    Validate that a string is a valid SQL identifier.
    Prevents SQL injection by ensuring only alphanumeric characters and underscores.
    Must start with a letter or underscore.
    """
    if not name:
        return False
    
    # SQL identifiers should match: [a-zA-Z_][a-zA-Z0-9_]*
    pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
    return bool(pattern.match(name))
