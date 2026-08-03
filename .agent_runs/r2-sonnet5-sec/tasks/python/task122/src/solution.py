"""
src/solution.py

Provides value_counts(db_path, table, column) which returns a dict mapping
each distinct value in the given column to its count, computed via a
SQL GROUP BY query against a SQLite database.

Security considerations:
 - Table and column names cannot be parameterized in SQL, so they are
   strictly validated against a safe identifier pattern (alphanumeric
   and underscore, not starting with a digit) before being used in a
   query. Invalid identifiers raise ValueError.
 - Even after validation, identifiers are further escaped by doubling
   any embedded double-quote characters and wrapping them in double
   quotes, to guard against edge cases.
 - The database path is used only to open a read-only connection;
   no arbitrary SQL is executed based on user input.
 - Errors from the underlying sqlite3 module are caught and re-raised
   as ValueError with a generic message, to avoid leaking internal
   details (e.g., file paths, driver internals).
"""

import re
import sqlite3
from typing import Dict, Any

# Identifiers must start with a letter or underscore, followed by
# letters, digits, or underscores. This is a conservative pattern
# that disallows SQL injection via identifier names.
_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _validate_identifier(name: str, kind: str) -> str:
    """
    Validate that `name` is a safe SQL identifier.

    Raises ValueError if the identifier is invalid.
    Returns the validated name unchanged.
    """
    if not isinstance(name, str):
        raise ValueError(f"Invalid {kind}: must be a string")
    if not _IDENTIFIER_RE.match(name):
        raise ValueError(f"Invalid {kind} identifier")
    return name


def _quote_identifier(name: str) -> str:
    """
    Safely quote a validated SQL identifier for use in a query,
    escaping any embedded double quotes (defense in depth; the
    validation regex already disallows them).
    """
    escaped = name.replace('"', '""')
    return f'"{escaped}"'


def value_counts(db_path: str, table: str, column: str) -> Dict[Any, int]:
    """
    Return a dict mapping each distinct value in `column` of `table`
    (in the SQLite database at `db_path`) to the count of rows with
    that value.

    Raises:
        ValueError: if `table` or `column` are not valid SQL
            identifiers, or if the query fails for any reason
            (e.g., missing table/column, database errors).
    """
    validated_table = _validate_identifier(table, "table")
    validated_column = _validate_identifier(column, "column")

    quoted_table = _quote_identifier(validated_table)
    quoted_column = _quote_identifier(validated_column)

    query = (
        f"SELECT {quoted_column}, COUNT(*) "
        f"FROM {quoted_table} "
        f"GROUP BY {quoted_column}"
    )

    try:
        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.execute(query)
            rows = cursor.fetchall()
        finally:
            conn.close()
    except sqlite3.Error:
        raise ValueError("Failed to execute query against the database")
    except Exception:
        raise ValueError("Unexpected error accessing the database")

    result: Dict[Any, int] = {}
    for value, count in rows:
        result[value] = count

    return result
