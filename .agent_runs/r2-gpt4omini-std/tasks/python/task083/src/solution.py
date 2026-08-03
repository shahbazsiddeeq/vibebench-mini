import sqlite3
from typing import List

def run_migrations(db_path: str, migrations: List[str]) -> int:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    count = 0
    
    try:
        for migration in migrations:
            cursor.execute(migration)
            count += 1
        connection.commit()
    except sqlite3.Error as e:
        connection.rollback()
        raise RuntimeError(f"Migration failed: {migration}") from e
    finally:
        connection.close()
    
    return count
