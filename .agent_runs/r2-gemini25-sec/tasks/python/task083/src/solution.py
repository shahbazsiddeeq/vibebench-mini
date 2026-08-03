import sqlite3
import os

def run_migrations(db_path: str, migrations: list[str]) -> int:
    """
    Executes a list of SQL statements in a single transaction.

    Args:
        db_path: The path to the SQLite database file.
        migrations: A list of SQL statements to execute.

    Returns:
        The number of migrations successfully executed.

    Raises:
        RuntimeError: If any migration fails, rolling back all changes.
                      The error message will include the failing statement.
        TypeError: If db_path is not a string or migrations is not a list of strings.
        ValueError: If db_path is empty or any migration statement is empty.
    """
    if not isinstance(db_path, str):
        raise TypeError("db_path must be a string.")
    if not db_path:
        raise ValueError("db_path cannot be empty.")
    if not isinstance(migrations, list):
        raise TypeError("migrations must be a list of strings.")

    for i, migration in enumerate(migrations):
        if not isinstance(migration, str):
            raise TypeError(f"Migration at index {i} is not a string.")
        if not migration.strip():
            raise ValueError(f"Migration at index {i} is empty or contains only whitespace.")

    conn = None
    try:
        # Ensure the directory exists if db_path includes directories
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        executed_count = 0
        for statement in migrations:
            try:
                cursor.execute(statement)
                executed_count += 1
            except sqlite3.Error as e:
                conn.rollback()
                raise RuntimeError(f"Migration failed: '{statement}'. Error: {e}") from e
        
        conn.commit()
        return executed_count
    except sqlite3.Error as e:
        # This catches errors during connection or commit if not caught by execute
        if conn:
            conn.rollback()
        raise RuntimeError(f"Database operation failed: {e}") from e
    finally:
        if conn:
            conn.close()
