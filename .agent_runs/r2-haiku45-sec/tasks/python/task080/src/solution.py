import sqlite3
import re
from typing import List, Dict, Any


def batch_insert(db_path: str, table: str, rows: List[Dict[str, Any]]) -> int:
    """
    Insert all rows into a table in a single transaction.
    
    Args:
        db_path: Path to the SQLite database file
        table: Name of the table to insert into
        rows: List of dictionaries representing rows to insert
        
    Returns:
        Number of rows inserted
        
    Raises:
        RuntimeError: If insertion fails or rows have inconsistent keys
        ValueError: If table name or column names contain invalid characters
    """
    
    # Validate inputs
    if not isinstance(db_path, str) or not db_path:
        raise ValueError("db_path must be a non-empty string")
    
    if not isinstance(table, str) or not table:
        raise ValueError("table must be a non-empty string")
    
    if not isinstance(rows, list):
        raise ValueError("rows must be a list")
    
    if len(rows) == 0:
        return 0
    
    # Validate table name - only alphanumeric and underscore
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table):
        raise ValueError(f"Invalid table name: {table}")
    
    # Get column names from first row
    first_row = rows[0]
    if not isinstance(first_row, dict):
        raise ValueError("Each row must be a dictionary")
    
    columns = list(first_row.keys())
    
    if not columns:
        raise ValueError("Rows must have at least one column")
    
    # Validate column names - only alphanumeric and underscore
    for col in columns:
        if not isinstance(col, str) or not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', col):
            raise ValueError(f"Invalid column name: {col}")
    
    # Validate all rows have the same keys
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            raise RuntimeError(f"Row {i} is not a dictionary")
        
        if set(row.keys()) != set(columns):
            raise RuntimeError(
                f"Row {i} has inconsistent keys. Expected {columns}, got {list(row.keys())}"
            )
    
    # Build the INSERT statement
    placeholders = ", ".join(["?" for _ in columns])
    column_names = ", ".join(columns)
    insert_sql = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"
    
    # Prepare data for insertion
    data_rows = []
    for row in rows:
        data_rows.append(tuple(row[col] for col in columns))
    
    # Execute transaction
    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute("BEGIN TRANSACTION")
            try:
                cursor = conn.executemany(insert_sql, data_rows)
                conn.commit()
                return cursor.rowcount
            except Exception as e:
                conn.rollback()
                raise RuntimeError(f"Failed to insert rows: {str(e)}") from e
    except sqlite3.Error as e:
        raise RuntimeError(f"Database error: {str(e)}") from e
    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError(f"Unexpected error during batch insert: {str(e)}") from e
