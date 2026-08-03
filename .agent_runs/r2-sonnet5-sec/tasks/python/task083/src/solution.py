"""
src/solution.py

A small, security-conscious SQLite migration runner.

The module exposes a single public function, `run_migrations`, which
executes a sequence of SQL statements against a SQLite database inside
a single transaction. If any statement fails, all changes are rolled
back and a `RuntimeError` is raised containing the offending statement
(but not raw internal exception details, to avoid leaking implementation
specifics).
"""

from __future__ import annotations

import sqlite3
from typing import Iterable, List


def _validate_db_path(db_path: object) -> str:
    """Validate that db_path is a non-empty string."""
    if not isinstance(db_path, str):
        raise TypeError("db_path must be a string")
    if not db_path.strip():
        raise ValueError("db_path must not be empty")
    return db_path


def _validate_migrations(migrations: object) -> List[str]:
    """Validate that migrations is an iterable of non-empty strings."""
    if migrations is None:
        raise TypeError("migrations must be an iterable of SQL statements")

    if isinstance(migrations, (str, bytes)):
        # A single string/bytes object is technically iterable of
        # characters/ints, which is not what we want.
        raise TypeError("migrations must be a list/iterable of SQL strings, not a single string")

    if not isinstance(migrations, Iterable):
        raise TypeError("migrations must be an iterable of SQL statements")

    result: List[str] = []
    for idx, stmt in enumerate(migrations):
        if not isinstance(stmt, str):
            raise TypeError(f"migration at index {idx} must be a string")
        if not stmt.strip():
            raise ValueError(f"migration at index {idx} must not be empty")
        result.append(stmt)

    return result


def run_migrations(db_path: str, migrations: Iterable[str]) -> int:
    """
    Execute a list of SQL statements against the SQLite database at
    `db_path`, all within a single transaction.

    Parameters
    ----------
    db_path : str
        Path to the SQLite database file.
    migrations : Iterable[str]
        A sequence of SQL statements to execute in order.

    Returns
    -------
    int
        The number of migrations successfully applied.

    Raises
    ------
    TypeError, ValueError
        If inputs are malformed.
    RuntimeError
        If any migration statement fails to execute. The message
        includes the failing statement. All changes made during the
        run are rolled back.
    """
    validated_db_path = _validate_db_path(db_path)
    validated_migrations = _validate_migrations(migrations)

    conn = None
    try:
        conn = sqlite3.connect(validated_db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        cursor.execute("BEGIN")
        applied = 0
        try:
            for stmt in validated_migrations:
                try:
                    cursor.execute(stmt)
                except sqlite3.Error:
                    # Do not leak internal driver error details; just
                    # report which statement failed.
                    raise RuntimeError(
                        f"Migration failed for statement: {stmt}"
                    )
                applied += 1

            conn.commit()
            return applied
        except RuntimeError:
            conn.rollback()
            raise
        except Exception:
            conn.rollback()
            raise RuntimeError("Migration failed due to an unexpected error")
    finally:
        if conn is not None:
            conn.close()
