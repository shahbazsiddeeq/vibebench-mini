# src/solution.py

import sqlite3

def run_migrations(db_path, migrations):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            for statement in migrations:
                cursor.execute(statement)
            conn.commit()
            return len(migrations)
        except sqlite3.Error as e:
            conn.rollback()
            raise RuntimeError(f"Failed to execute statement: {statement}") from e
        finally:
            cursor.close()
            conn.close()
    except sqlite3.Error as e:
        raise RuntimeError("Database connection error") from e
