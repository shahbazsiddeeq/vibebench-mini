import sqlite3
from pathlib import Path
from typing import List


def run_migrations(db_path: str, migrations: List[str]) -> int:
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
    # Validate inputs
    if not isinstance(db_path, str):
        raise ValueError("db_path must be a string")
    
    if not isinstance(migrations, list):
        raise ValueError("migrations must be a list")
    
    # Validate db_path to prevent path traversal
    try:
        resolved_path = Path(db_path).resolve()
    except (ValueError, OSError) as e:
        raise ValueError(f"Invalid database path: {e}")
    
    # Validate all migrations are strings
    for i, migration in enumerate(migrations):
        if not isinstance(migration, str):
            raise ValueError(f"Migration at index {i} must be a string")
    
    conn = None
    try:
        # Connect to database
        conn = sqlite3.connect(str(resolved_path))
        cursor = conn.cursor()
        
        # Execute migrations in a transaction
        count = 0
        for migration in migrations:
            try:
                cursor.execute(migration)
                count += 1
            except sqlite3.Error as e:
                # Rollback on error
                conn.rollback()
                # Raise RuntimeError with the failing statement
                raise RuntimeError(f"Migration failed: {migration}") from e
        
        # Commit transaction if all migrations succeed
        conn.commit()
        return count
        
    except RuntimeError:
        # Re-raise RuntimeError as-is
        raise
    except Exception as e:
        # Wrap other exceptions
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
        raise RuntimeError(f"Unexpected error during migration: {type(e).__name__}") from e
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass
