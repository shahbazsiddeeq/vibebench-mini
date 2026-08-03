import sqlite3


def run_migrations(db_path, migrations):
    """
    Execute a list of SQL statements in a single transaction.
    
    Args:
        db_path: Path to the SQLite database file
        migrations: List of SQL statements to execute
        
    Returns:
        Count of successfully executed migrations
        
    Raises:
        RuntimeError: If any migration fails, with the failing statement in the message
    """
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("BEGIN TRANSACTION")
        
        for i, migration in enumerate(migrations):
            try:
                cursor.execute(migration)
            except sqlite3.Error as e:
                conn.rollback()
                raise RuntimeError(f"Migration failed: {migration}") from e
        
        conn.commit()
        return len(migrations)
    except RuntimeError:
        raise
    except Exception as e:
        conn.rollback()
        raise RuntimeError(str(e)) from e
    finally:
        conn.close()
