# src/solution.py

import sqlite3

def batch_insert(db_path, table, rows):
    if not rows:
        return 0

    # Validate column names to prevent SQL injection
    for row in rows:
        for column in row.keys():
            if not column.isidentifier():
                raise ValueError("Invalid column name detected.")

    # Extract column names and ensure all rows have the same keys
    columns = rows[0].keys()
    for row in rows:
        if row.keys() != columns:
            raise RuntimeError("Mismatched row keys.")

    placeholders = ', '.join('?' for _ in columns)
    column_names = ', '.join(columns)

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("BEGIN")
            cursor.executemany(
                f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})",
                [tuple(row[col] for col in columns) for row in rows]
            )
            conn.commit()
            return len(rows)
    except sqlite3.Error as e:
        raise RuntimeError(f"Database error: {e}")
