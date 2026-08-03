import sqlite3
import re

def upsert(db_path, table, record, key):
    # Validate identifiers
    if not _is_valid_identifier(table) or not _is_valid_identifier(key):
        raise ValueError("Invalid table or key identifier.")
    
    if key not in record:
        raise KeyError(f"Key '{key}' not found in record.")
    
    # Prepare the columns and values for the SQL statement
    columns = [col for col in record if col != key]
    if not columns:
        # If there are no columns to update, we do nothing
        return
    
    # Create the SQL statement
    columns_str = ', '.join(f'"{col}" = ?' for col in columns)
    sql = f'INSERT INTO "{table}" ("{key}", {columns_str}) VALUES (?, {", ".join("?" for _ in columns)}) ' \
          f'ON CONFLICT("{key}") DO UPDATE SET {columns_str};'
    
    # Prepare the values for the SQL statement
    values = [record[key]] + [record[col] for col in columns]
    
    # Execute the SQL statement
    with sqlite3.connect(db_path) as conn:
        conn.execute(sql, values)

def _is_valid_identifier(identifier):
    return bool(re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', identifier))
