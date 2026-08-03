import sqlite3
import re

def bulk_update(conn: sqlite3.Connection, table: str, key_column: str, rows: list[dict]) -> int:
    # Validate identifiers
    identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    
    if not identifier_pattern.match(table):
        raise ValueError("Invalid table name")
    if not identifier_pattern.match(key_column):
        raise ValueError("Invalid key column name")
    
    if not isinstance(rows, list):
        raise ValueError("Rows must be a list")
    
    if not rows:
        return 0
    
    total_modified = 0
    
    try:
        with conn:
            for row in rows:
                if key_column not in row:
                    raise ValueError(f"Missing key column '{key_column}' in row")
                
                set_columns = {k: v for k, v in row.items() if k != key_column}
                
                if not set_columns:
                    raise ValueError("Each row must have at least one column to set")
                
                for col in set_columns:
                    if not identifier_pattern.match(col):
                        raise ValueError(f"Invalid column name '{col}'")
                
                set_clause = ", ".join(f'"{col}" = ?' for col in set_columns)
                sql = f'UPDATE "{table}" SET {set_clause} WHERE "{key_column}" = ?'
                
                values = list(set_columns.values()) + [row[key_column]]
                
                cursor = conn.execute(sql, values)
                total_modified += cursor.rowcount
    
    except sqlite3.Error as e:
        raise RuntimeError("Database error occurred") from e
    
    return total_modified
