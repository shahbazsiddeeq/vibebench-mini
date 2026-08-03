"""
src/solution.py

Secure SQLite row pagination utility.

Provides `paginate(db_path, table, page, page_size)` which returns a page of
rows (as plain tuples) from an existing SQLite table, ordered by rowid.
"""

import re
import sqlite3
from typing import List, Tuple, Any

# Strict identifier pattern: must start with a letter or underscore,
# followed by letters, digits, or underscores.
_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _validate_identifier(name: str) -> str:
    """
    Validate that `name` is a safe SQL identifier.

    Raises:
        ValueError: if `name` is not a string or does not match the
            allowed identifier pattern.
    """
    if not isinstance(name, str) or not _IDENTIFIER_RE.match(name):
        raise ValueError("Invalid table name")
    return name


def _validate_positive_int(value: Any, name: str) -> int:
    """
    Validate that `value` is an integer >= 1 (bool excluded).

    Raises:
        ValueError: if `value` is not a valid positive integer.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"Invalid {name}")
    if value < 1:
        raise ValueError(f"Invalid {name}")
    return value


def paginate(
    db_path: str,
    table: str,
    page: int,
    page_size: int,
) -> List[Tuple[Any, ...]]:
    """
    Return a 1-based page of rows from `table` in the SQLite database at
    `db_path`, ordered by rowid, using LIMIT/OFFSET.

    Args:
        db_path: Path to the SQLite database file.
        table: Name of the table to query. Must be a valid identifier
            matching ``[A-Za-z_][A-Za-z0-9_]*``.
        page: 1-based page number (must be >= 1).
        page_size: Number of rows per page (must be >= 1).

    Returns:
        A list of tuples, each tuple containing the column values (in
        SELECT * order) for a row on the requested page. Returns an empty
        list if the page is past the end of the table.

    Raises:
        ValueError: If `table` is not a valid identifier, or if `page` or
            `page_size` is less than 1, or if the database/table cannot
            be accessed.
    """
    validated_table = _validate_identifier(table)
    validated_page = _validate_positive_int(page, "page")
    validated_page_size = _validate_positive_int(page_size, "page_size")

    if not isinstance(db_path, str) or not db_path:
        raise ValueError("Invalid database path")

    offset = (validated_page - 1) * validated_page_size

    # Table name is validated against a strict identifier regex above,
    # so it is safe to interpolate into the SQL string. LIMIT/OFFSET
    # values are passed as parameters to avoid injection.
    query = f'SELECT * FROM "{validated_table}" ORDER BY rowid LIMIT ? OFFSET ?'  # noqa: S608

    try:
        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.execute(query, (validated_page_size, offset))
            rows = cursor.fetchall()
        finally:
            conn.close()
    except sqlite3.Error as exc:
        # Avoid leaking internal details (e.g., file paths, SQL text).
        raise ValueError("Unable to query the specified table") from exc

    return [tuple(row) for row in rows]
