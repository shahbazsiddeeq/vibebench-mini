import sqlite3


def run_migrations(db_path, migrations):
    """
    Execute a list of SQL statements in a single transaction.
    
    Args:
        db_path: Path to the SQLite database file
        migrations: List of SQL statements to execute
    
    Returns:
        Count of migrations executed
    
    Raises:
        RuntimeError: If any migration fails, with the failing statement in the message
    """
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        count = 0
        
        for migration in migrations:
            try:
                cursor.execute(migration)
                count += 1
            except Exception as e:
                conn.rollback()
                raise RuntimeError(f"Migration failed: {migration}") from e
        
        conn.commit()
        return count
    finally:
        conn.close()
