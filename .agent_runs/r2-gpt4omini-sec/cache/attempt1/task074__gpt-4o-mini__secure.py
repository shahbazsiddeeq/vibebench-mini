import sqlite3
import re

def _validate_identifier(identifier):
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', identifier):
        raise ValueError(f"Invalid identifier: {identifier}")

def upsert(db_path, table, record, key):
    _validate_identifier(table)
    _validate_identifier(key)
    
    if key not in record:
        raise KeyError(f"Key '{key}' not found in record")

    # Prepare the columns and values for the SQL statement
    columns = [col for col in record.keys() if col != key]
    if not columns:
        return  # If record only contains the key, do nothing

    # Create the SQL statement
    set_clause = ', '.join(f'"{col}" = ?' for col in columns)
    sql = f'INSERT INTO "{table}" ("{key}", {set_clause}) VALUES (?, {", ".join("?" for _ in columns)}) ON CONFLICT("{key}") DO UPDATE SET {set_clause}'

    # Prepare the values for the SQL statement
    values = [record[key]] + [record[col] for col in columns]

    # Execute the SQL statement
    with sqlite3.connect(db_path) as conn:
        conn.execute(sql, values)
        conn.commit()
