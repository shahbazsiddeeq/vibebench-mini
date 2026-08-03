import sqlite3
import re


def batch_insert(db_path, table, rows):
    """
    Insert all rows into a table in a single transaction.
    
    Args:
        db_path: Path to the SQLite database
        table: Name of the table to insert into
        rows: List of dictionaries representing rows to insert
        
    Returns:
        Number of rows inserted
        
    Raises:
        RuntimeError: If insertion fails or table doesn't exist
        ValueError: If column names contain invalid characters
    """
    if not rows:
        return 0
    
    # Validate table name (basic check for SQL injection)
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table):
        raise ValueError(f"Invalid table name: {table}")
    
    # Get column names from first row
    columns = list(rows[0].keys())
    
    # Validate column names
    for col in columns:
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', col):
            raise ValueError(f"Invalid column name: {col}")
    
    # Verify all rows have the same keys
    for i, row in enumerate(rows):
        if set(row.keys()) != set(columns):
            raise RuntimeError(f"Row {i} has mismatched keys. Expected {columns}, got {list(row.keys())}")
    
    try:
        with sqlite3.connect(db_path) as conn:
            # Start transaction
            conn.execute("BEGIN TRANSACTION")
            
            try:
                # Build INSERT statement
                placeholders = ','.join(['?' for _ in columns])
                col_names = ','.join(columns)
                insert_sql = f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})"
                
                # Insert all rows
                for row in rows:
                    values = [row[col] for col in columns]
                    conn.execute(insert_sql, values)
                
                # Commit transaction
                conn.commit()
                return len(rows)
            except Exception as e:
                # Rollback on any error
                conn.rollback()
                raise RuntimeError(f"Failed to insert rows: {str(e)}") from e
    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError(f"Database operation failed: {str(e)}") from e
