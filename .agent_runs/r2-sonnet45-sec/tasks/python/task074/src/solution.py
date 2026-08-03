import sqlite3
import re


def upsert(db_path, table, record, key):
    """
    Insert or update a record in a SQLite table.
    
    Args:
        db_path: Path to the SQLite database file
        table: Table name (must be valid identifier)
        record: Dictionary of column-value pairs
        key: Key column name (must be in record and be valid identifier)
    
    Raises:
        ValueError: If table, key, or any record key is not a valid identifier
        KeyError: If key is not in record
    """
    # Validate that key is in record
    if key not in record:
        raise KeyError(f"Key '{key}' not found in record")
    
    # Validate identifiers
    identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    
    if not identifier_pattern.match(table):
        raise ValueError(f"Invalid table name: {table}")
    
    if not identifier_pattern.match(key):
        raise ValueError(f"Invalid key name: {key}")
    
    for column in record.keys():
        if not identifier_pattern.match(column):
            raise ValueError(f"Invalid column name: {column}")
    
    # Build the INSERT statement with ON CONFLICT clause
    columns = list(record.keys())
    
    # Quote identifiers by wrapping in double quotes
    quoted_table = f'"{table}"'
    quoted_columns = [f'"{col}"' for col in columns]
    quoted_key = f'"{key}"'
    
    # Placeholders for values
    placeholders = ['?' for _ in columns]
    
    # Build the base INSERT statement
    insert_sql = f"INSERT INTO {quoted_table} ({', '.join(quoted_columns)}) VALUES ({', '.join(placeholders)})"
    
    # Build the ON CONFLICT clause
    # We need to update all columns except the key
    update_columns = [col for col in columns if col != key]
    
    if update_columns:
        # Build SET clause for UPDATE
        set_clause = ', '.join([f'"{col}" = excluded."{col}"' for col in update_columns])
        conflict_sql = f" ON CONFLICT({quoted_key}) DO UPDATE SET {set_clause}"
    else:
        # If record only contains the key, do nothing on conflict
        conflict_sql = f" ON CONFLICT({quoted_key}) DO NOTHING"
    
    full_sql = insert_sql + conflict_sql
    
    # Extract values in the same order as columns
    values = [record[col] for col in columns]
    
    # Execute the statement
    with sqlite3.connect(db_path) as conn:
        conn.execute(full_sql, values)
        conn.commit()
