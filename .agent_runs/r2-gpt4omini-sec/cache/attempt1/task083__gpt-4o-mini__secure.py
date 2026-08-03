# src/solution.py

import sqlite3
from typing import List

def run_migrations(db_path: str, migrations: List[str]) -> int:
    # Validate inputs
    if not isinstance(db_path, str) or not db_path.strip():
        raise ValueError("Invalid database path.")
    if not isinstance(migrations, list) or not all(isinstance(m, str) for m in migrations):
        raise ValueError("Migrations must be a list of SQL statements as strings.")

    # Connect to the SQLite database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    try:
        # Begin a transaction
        cursor.execute("BEGIN")
        count = 0
        
        for migration in migrations:
            # Execute each migration
            cursor.execute(migration)
            count += 1
        
        # Commit the transaction
        connection.commit()
        return count

    except sqlite3.Error as e:
        # Rollback on error
        connection.rollback()
        # Raise a RuntimeError with the failing statement
        raise RuntimeError(f"Migration failed: {migration}") from e

    finally:
        # Close the connection
        connection.close()
