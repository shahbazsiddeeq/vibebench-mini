import sqlite3
from pathlib import Path


def run_migrations(db_path, migrations):
    """
    Execute a list of SQL statements in a single transaction.
    
    Args:
        db_path: Path to the SQLite database file
        migrations: List of SQL statement strings to execute
        
    Returns:
        Count of successfully executed migrations
        
    Raises:
        RuntimeError: If any migration fails, with the failing statement in the message
    """
    # Validate inputs
    if not isinstance(db_path, (str, Path)):
        raise TypeError("db_path must be a string or Path")
    
    if not isinstance(migrations, list):
        raise TypeError("migrations must be a list")
    
    # Validate all migrations are strings
    for migration in migrations:
        if not isinstance(migration, str):
            raise TypeError("All migrations must be strings")
    
    db_path = str(db_path)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            # Start transaction
            cursor.execute("BEGIN TRANSACTION")
            
            count = 0
            for migration in migrations:
                try:
                    cursor.execute(migration)
                    count += 1
                except sqlite3.Error as e:
                    # Rollback on error
                    conn.rollback()
                    raise RuntimeError(f"Migration failed: {migration}") from e
            
            # Commit transaction
            conn.commit()
            return count
            
        except RuntimeError:
            # Re-raise RuntimeError as-is
            raise
        except Exception as e:
            # Rollback any other unexpected errors
            conn.rollback()
            raise RuntimeError(f"Unexpected error during migrations: {str(e)}") from e
        finally:
            cursor.close()
            
    finally:
        conn.close()
