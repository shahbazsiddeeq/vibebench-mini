import sqlite3
import re

def upsert(db_path, table, record, key):
    # Validate identifiers
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', table):
        raise ValueError(f"Invalid table name: {table}")
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', key):
        raise ValueError(f"Invalid key name: {key}")
    if key not in record:
        raise KeyError(f"Key '{key}' not found in record.")

    # Prepare the columns and values for the SQL statement
    columns = [col for col in record if col != key]
    if not columns:
        # If there are no columns to update, we do nothing
        return

    # Create the SQL statement
    columns_str = ', '.join(f'"{col}" = ?' for col in columns)
    sql = f'INSERT INTO "{table}" ("{key}", {", ".join(f"{col}" for col in columns)}) VALUES (?, {", ".join("?" for _ in columns)}) ' \
          f'ON CONFLICT("{key}") DO UPDATE SET {columns_str};'

    # Prepare the values for the SQL statement
    values = [record[key]] + [record[col] for col in columns] + [record[col] for col in columns]

    # Execute the SQL statement
    with sqlite3.connect(db_path) as conn:
        conn.execute(sql, values)
