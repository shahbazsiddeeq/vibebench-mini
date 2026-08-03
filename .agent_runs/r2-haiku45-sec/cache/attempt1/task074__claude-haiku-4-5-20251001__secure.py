import sqlite3
import re
from typing import Any


def _is_valid_identifier(name: str) -> bool:
    """Check if a name is a valid SQL identifier."""
    return bool(re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name))


def upsert(db_path: str, table: str, record: dict[str, Any], key: str) -> None:
    """
    Insert or update a record in a SQLite table.
    
    Args:
        db_path: Path to the SQLite database file
        table: Table name (must be a valid identifier)
        record: Dictionary of column names to values
        key: Key column name (must be in record and a valid identifier)
    
    Raises:
        ValueError: If table, key, or record keys are not valid identifiers
        KeyError: If key is not in record
    """
    # Validate identifiers
    if not _is_valid_identifier(table):
        raise ValueError(f"Invalid table name: {table}")
    
    if not _is_valid_identifier(key):
        raise ValueError(f"Invalid key column name: {key}")
    
    # Check that key is in record
    if key not in record:
        raise KeyError(f"Key '{key}' not found in record")
    
    # Validate all column names in record
    for col_name in record.keys():
        if not _is_valid_identifier(col_name):
            raise ValueError(f"Invalid column name: {col_name}")
    
    # Build the upsert query using ON CONFLICT
    # We use INSERT OR REPLACE with a subquery to preserve omitted columns
    columns = list(record.keys())
    placeholders = ', '.join(['?' for _ in columns])
    column_list = ', '.join([f'"{col}"' for col in columns])
    
    # Build the SET clause for UPDATE, excluding the key column
    update_columns = [col for col in columns if col != key]
    if update_columns:
        set_clause = ', '.join([f'"{col}" = excluded."{col}"' for col in update_columns])
        query = f"""
            INSERT INTO "{table}" ({column_list})
            VALUES ({placeholders})
            ON CONFLICT("{key}") DO UPDATE SET {set_clause}
        """
    else:
        # If only the key is provided, do nothing on conflict
        query = f"""
            INSERT OR IGNORE INTO "{table}" ({column_list})
            VALUES ({placeholders})
        """
    
    values = [record[col] for col in columns]
    
    with sqlite3.connect(db_path) as conn:
        conn.execute(query, values)
        conn.commit()
