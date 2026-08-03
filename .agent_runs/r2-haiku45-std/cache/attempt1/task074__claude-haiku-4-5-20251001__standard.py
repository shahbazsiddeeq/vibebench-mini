import sqlite3
import re


def upsert(db_path, table, record, key):
    """
    Inserts or updates a record in a SQLite table.
    
    Args:
        db_path: Path to the SQLite database
        table: Table name (must be valid identifier)
        record: Dictionary of column names to values
        key: Key column name (must be in record and valid identifier)
    
    Raises:
        ValueError: If table, key, or record keys are not valid identifiers
        KeyError: If key is not in record
    """
    
    # Validate identifier pattern
    identifier_pattern = r'^[A-Za-z_][A-Za-z0-9_]*$'
    
    # Check table name
    if not re.match(identifier_pattern, table):
        raise ValueError(f"Invalid table name: {table}")
    
    # Check key name
    if not re.match(identifier_pattern, key):
        raise ValueError(f"Invalid key name: {key}")
    
    # Check that key is in record
    if key not in record:
        raise KeyError(f"Key '{key}' not found in record")
    
    # Check all record keys are valid identifiers
    for col in record.keys():
        if not re.match(identifier_pattern, col):
            raise ValueError(f"Invalid column name: {col}")
    
    # Build the upsert query using ON CONFLICT
    # We need to update all columns except the key on conflict
    columns = list(record.keys())
    placeholders = ', '.join(['?' for _ in columns])
    
    # For the UPDATE part, we update all columns except the key
    update_columns = [col for col in columns if col != key]
    update_clause = ', '.join([f'"{col}" = excluded."{col}' for col in update_columns])
    
    # Build column names with quotes
    quoted_columns = ', '.join([f'"{col}"' for col in columns])
    
    # Build the INSERT OR IGNORE ... ON CONFLICT DO UPDATE query
    if update_clause:
        query = f'''
            INSERT INTO "{table}" ({quoted_columns})
            VALUES ({placeholders})
            ON CONFLICT("{key}") DO UPDATE SET {update_clause}
        '''
    else:
        # If only key is in record, do nothing on conflict
        query = f'''
            INSERT OR IGNORE INTO "{table}" ({quoted_columns})
            VALUES ({placeholders})
        '''
    
    # Extract values in the same order as columns
    values = [record[col] for col in columns]
    
    # Execute the query
    with sqlite3.connect(db_path) as conn:
        conn.execute(query, values)
        conn.commit()
