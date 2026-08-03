import sqlite3
from typing import List, Dict
import secrets

def batch_insert(db_path: str, table: str, rows: List[Dict[str, any]]) -> int:
    if not rows:
        return 0

    # Validate table name to prevent SQL injection
    if not table.isidentifier():
        raise ValueError("Invalid table name")

    # Validate column names to prevent SQL injection
    columns = rows[0].keys()
    for column in columns:
        if not column.isidentifier():
            raise ValueError("Invalid column name")

    # Ensure all rows have the same keys
    for row in rows:
        if set(row.keys()) != set(columns):
            raise RuntimeError("Mismatched row keys")

    placeholders = ", ".join("?" for _ in columns)
    column_names = ", ".join(columns)
    query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"

    try:
        with sqlite3.connect(db_path) as conn:
            conn.isolation_level = None  # Use explicit transactions
            conn.execute("BEGIN")
            cursor = conn.executemany(query, [tuple(row[col] for col in columns) for row in rows])
            conn.commit()
            return cursor.rowcount
    except sqlite3.Error as e:
        conn.rollback()
        raise RuntimeError("Database operation failed") from e
