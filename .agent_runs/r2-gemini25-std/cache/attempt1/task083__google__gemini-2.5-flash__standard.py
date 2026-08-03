import sqlite3

def run_migrations(db_path: str, migrations: list[str]) -> int:
    """
    Executes a list of SQL statements in a single transaction.

    Args:
        db_path: The path to the SQLite database file.
        migrations: A list of SQL statements to execute.

    Returns:
        The number of successfully executed migrations.

    Raises:
        RuntimeError: If any SQL statement fails, with the failing statement
                      included in the error message. All changes are rolled back.
    """
    conn = None
    try:
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
        # This catch is for connection errors or other unexpected sqlite3 errors
        # not caught by the inner try-except for individual statements.
        # In most cases, the inner catch will handle statement failures.
        raise RuntimeError(f"Database operation failed: {e}") from e
    finally:
        if conn:
            conn.close()
