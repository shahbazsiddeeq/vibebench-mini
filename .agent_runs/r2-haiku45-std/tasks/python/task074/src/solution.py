import sqlite3
import re


def upsert(db_path, table, record, key):
    """
    Insert or update a record in a SQLite table.
    
    Args:
        db_path: Path to the SQLite database
        table: Table name (must be valid identifier)
        record: Dictionary of column names to values (must include key)
        key: Key column name for conflict resolution (must be valid identifier)
    
    Raises:
        ValueError: If table, key, or record keys are not valid identifiers
        KeyError: If key is not in record
    """
    
    # Validate identifier pattern
    identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    
    def is_valid_identifier(name):
        return identifier_pattern.match(name) is not None
    
    # Validate table name
    if not is_valid_identifier(table):
        raise ValueError(f"Invalid table name: {table}")
    
    # Validate key column name
    if not is_valid_identifier(key):
        raise ValueError(f"Invalid key column name: {key}")
    
    # Check that key is in record
    if key not in record:
        raise KeyError(f"Key '{key}' not found in record")
    
    # Validate all column names in record
    for col in record.keys():
        if not is_valid_identifier(col):
            raise ValueError(f"Invalid column name: {col}")
    
    # Get columns and values
    columns = list(record.keys())
    placeholders = ', '.join(['?' for _ in columns])
    quoted_columns = ', '.join([f'"{col}"' for col in columns])
    
    # Build the SET clause for columns other than key
    update_columns = [col for col in columns if col != key]
    
    if update_columns:
        # Build SET clause with proper quoting
        set_clause = ', '.join([f'"{col}" = ?' for col in update_columns])
        
        # Build the INSERT OR IGNORE ... ON CONFLICT DO UPDATE query
        query = f'''
            INSERT INTO "{table}" ({quoted_columns})
            VALUES ({placeholders})
            ON CONFLICT("{key}") DO UPDATE SET {set_clause}
        '''
        
        # Extract values: first all columns for INSERT, then update columns for SET
        values = [record[col] for col in columns] + [record[col] for col in update_columns]
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
