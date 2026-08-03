import sqlite3
import re


def batch_insert(db_path, table, rows):
    """
    Insert all rows into the specified table in a single transaction.
    
    Args:
        db_path: Path to the SQLite database file
        table: Name of the table to insert into
        rows: List of dictionaries, where each dict represents a row
        
    Returns:
        Number of rows inserted
        
    Raises:
        RuntimeError: On database errors or mismatched row keys
        ValueError: On potential SQL injection attempts in column names
    """
    if not rows:
        return 0
    
    # Validate that all rows have the same keys
    first_keys = set(rows[0].keys())
    for i, row in enumerate(rows):
        if set(row.keys()) != first_keys:
            raise RuntimeError(f"Row {i} has different keys than the first row")
    
    # Validate column names to prevent SQL injection
    # Column names should be valid identifiers (alphanumeric and underscore)
    for column in first_keys:
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', column):
            raise ValueError(f"Invalid column name: {column}")
    
    # Get column names in a consistent order
    columns = sorted(first_keys)
    
    # Build the INSERT statement
    placeholders = ', '.join(['?' for _ in columns])
    column_names = ', '.join(columns)
    insert_sql = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"
    
    try:
        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.cursor()
            
            # Insert all rows
            for row in rows:
                values = [row[col] for col in columns]
                cursor.execute(insert_sql, values)
            
            # Commit the transaction
            conn.commit()
            
            # Return the count of inserted rows
            return len(rows)
            
        except Exception as e:
            # Rollback on any error
            conn.rollback()
            raise RuntimeError(f"Database error: {e}")
        finally:
            conn.close()
            
    except sqlite3.Error as e:
        raise RuntimeError(f"Database connection error: {e}")
