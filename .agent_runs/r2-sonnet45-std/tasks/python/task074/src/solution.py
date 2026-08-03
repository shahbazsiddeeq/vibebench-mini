import sqlite3
import re


def upsert(db_path, table, record, key):
    """
    Insert record into a SQLite table, or update the existing row on conflict.
    
    Args:
        db_path: Path to the SQLite database
        table: Table name (must be valid identifier)
        record: Dictionary of column-value pairs
        key: Key column name (must be in record and be valid identifier)
    
    Raises:
        ValueError: If table, key, or any record key is not a valid identifier
        KeyError: If key is not in record
    """
    # Validate identifier pattern
    identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    
    def is_valid_identifier(name):
        return identifier_pattern.match(name) is not None
    
    # Validate table name
    if not is_valid_identifier(table):
        raise ValueError(f"Invalid table name: {table}")
    
    # Validate key is in record
    if key not in record:
        raise KeyError(f"Key '{key}' not in record")
    
    # Validate key name
    if not is_valid_identifier(key):
        raise ValueError(f"Invalid key name: {key}")
    
    # Validate all column names in record
    for col in record.keys():
        if not is_valid_identifier(col):
            raise ValueError(f"Invalid column name: {col}")
    
    # Build the INSERT statement with ON CONFLICT clause
    columns = list(record.keys())
    placeholders = ', '.join(['?'] * len(columns))
    column_names = ', '.join([f'"{col}"' for col in columns])
    
    # Build UPDATE SET clause (exclude the key column)
    update_columns = [col for col in columns if col != key]
    
    if update_columns:
        # If there are columns to update besides the key
        update_set = ', '.join([f'"{col}" = excluded."{col}"' for col in update_columns])
        sql = f'''
            INSERT INTO "{table}" ({column_names})
            VALUES ({placeholders})
            ON CONFLICT ("{key}") DO UPDATE SET {update_set}
        '''
    else:
        # If record contains only the key, do nothing on conflict
        sql = f'''
            INSERT INTO "{table}" ({column_names})
            VALUES ({placeholders})
            ON CONFLICT ("{key}") DO NOTHING
        '''
    
    # Execute the query with bound parameters
    values = [record[col] for col in columns]
    
    with sqlite3.connect(db_path) as conn:
        conn.execute(sql, values)
        conn.commit()
