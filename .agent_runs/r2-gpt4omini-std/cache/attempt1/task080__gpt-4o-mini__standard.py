import sqlite3

def batch_insert(db_path, table, rows):
    if not rows:
        return 0

    # Check for SQL injection in column names
    for row in rows:
        for key in row.keys():
            if not isinstance(key, str) or ';' in key or '--' in key:
                raise ValueError("Invalid column name detected.")

    # Check for consistent keys in all rows
    keys = rows[0].keys()
    for row in rows:
        if row.keys() != keys:
            raise RuntimeError("Mismatched row keys.")

    placeholders = ', '.join('?' * len(keys))
    columns = ', '.join(keys)

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"BEGIN TRANSACTION;")
            cursor.executemany(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", 
                               [tuple(row[key] for key in keys) for row in rows])
            conn.commit()
            return len(rows)
    except Exception as e:
        raise RuntimeError("Database operation failed.") from e
