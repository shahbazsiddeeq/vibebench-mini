"""SQLite migration runner."""

from __future__ import annotations

import os
import sqlite3
from collections.abc import Iterable
from typing import Union

PathType = Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]


def run_migrations(db_path: PathType, migrations: Iterable[str]) -> int:
    """Execute SQL migrations atomically and return the number executed.

    If a statement fails, all changes are rolled back and a RuntimeError
    identifying the failing statement is raised.
    """
    try:
        normalized_path = os.fspath(db_path)
    except TypeError:
        raise TypeError("db_path must be a string, bytes, or path-like object") from None

    if not isinstance(normalized_path, (str, bytes)):
        raise TypeError("db_path must resolve to a string or bytes path")

    if isinstance(normalized_path, str) and "\x00" in normalized_path:
        raise ValueError("db_path contains a null character")
    if isinstance(normalized_path, bytes) and b"\x00" in normalized_path:
        raise ValueError("db_path contains a null byte")

    if isinstance(migrations, (str, bytes)) or not isinstance(migrations, Iterable):
        raise TypeError("migrations must be an iterable of SQL strings")

    try:
        statements = list(migrations)
    except Exception:
        raise TypeError("migrations could not be read") from None

    for statement in statements:
        if not isinstance(statement, str):
            raise TypeError("each migration must be a SQL string")

    try:
        connection = sqlite3.connect(normalized_path, isolation_level=None)
    except (sqlite3.Error, OSError, ValueError):
        raise RuntimeError("unable to open the database") from None

    current_statement: str | None = None
    try:
        connection.execute("BEGIN")
        for current_statement in statements:
            connection.execute(current_statement)
        connection.execute("COMMIT")
        return len(statements)
    except Exception:
        try:
            if connection.in_transaction:
                connection.execute("ROLLBACK")
        except sqlite3.Error:
            pass

        if current_statement is None:
            raise RuntimeError("migration transaction failed before execution") from None
        raise RuntimeError(
            f"migration failed for statement: {current_statement}"
        ) from None
    finally:
        connection.close()
