import sqlite3
import re
from secrets import SystemRandom

def upsert(db_path, table, record, key):
    # Validate identifiers
    identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    
    if not identifier_pattern.match(table):
        raise ValueError(f"Invalid table name: {table}")
    
    if not identifier_pattern.match(key):
        raise ValueError(f"Invalid key name: {key}")
    
    for column in record.keys():
        if not identifier_pattern.match(column):
            raise ValueError(f"Invalid column name: {column}")
    
    # Check if key is in record
    if key not in record:
        raise KeyError(f"Key '{key}' not found in record")
    
    # Prepare columns and placeholders
    columns = list(record.keys())
    placeholders = ', '.join(['?'] * len(columns))
    update_columns = ', '.join(
        [f'"{col}" = EXCLUDED."{col}"' for col in columns if col != key]
    )
    
    # Construct SQL statement
    sql = f'''
    INSERT INTO "{table}" ({', '.join(f'"{col}"' for col in columns)})
    VALUES ({placeholders})
    ON CONFLICT("{key}") DO UPDATE SET
    {update_columns}
    '''
    
    # Execute SQL statement
    with sqlite3.connect(db_path) as conn:
        conn.execute(sql, tuple(record[col] for col in columns))
