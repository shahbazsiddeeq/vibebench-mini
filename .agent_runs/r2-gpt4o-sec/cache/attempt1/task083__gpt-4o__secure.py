import sqlite3
from typing import List

def run_migrations(db_path: str, migrations: List[str]) -> int:
    if not isinstance(db_path, str) or not isinstance(migrations, list):
        raise ValueError("Invalid input types.")
    
    for migration in migrations:
        if not isinstance(migration, str):
            raise ValueError("All migrations must be strings.")
    
    connection = sqlite3.connect(db_path)
    try:
        with connection:
            cursor = connection.cursor()
            for migration in migrations:
                try:
                    cursor.execute(migration)
                except sqlite3.DatabaseError as e:
                    raise RuntimeError(f"Failed to execute migration: {migration}") from e
            return len(migrations)
    finally:
        connection.close()
