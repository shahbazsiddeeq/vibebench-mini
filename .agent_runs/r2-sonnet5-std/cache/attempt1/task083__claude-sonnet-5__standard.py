import sqlite3


def run_migrations(db_path, migrations):
    conn = sqlite3.connect(db_path)
    count = 0
    try:
        cursor = conn.cursor()
        for statement in migrations:
            try:
                cursor.execute(statement)
            except sqlite3.Error as e:
                conn.rollback()
                raise RuntimeError(
                    f"Migration failed on statement: {statement!r} - {e}"
                ) from e
            count += 1
        conn.commit()
        return count
    finally:
        conn.close()
