import sqlite3


def value_counts(db_path: str, table: str, column: str) -> dict:
    """
    Returns a dict mapping each distinct value in the given column to its count,
    computed with GROUP BY. Raises ValueError if table or column is an invalid identifier.

    Args:
        db_path: The path to the SQLite database file.
        table: The name of the table.
        column: The name of the column.

    Returns:
        A dictionary where keys are distinct column values and values are their counts.

    Raises:
        ValueError: If table or column is an invalid identifier.
    """
    if not (table.isidentifier() and column.isidentifier()):
        raise ValueError("Table or column name contains invalid characters.")

    counts = {}
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        try:
            query = f"SELECT {column}, COUNT(*) FROM {table} GROUP BY {column}"
            cursor.execute(query)
            for value, count in cursor.fetchall():
                counts[value] = count
        except sqlite3.OperationalError as e:
            # Catch errors like "no such table" or "no such column"
            # and re-raise as ValueError for consistency with the spec.
            if f"no such table: {table}" in str(e) or f"no such column: {column}" in str(e):
                raise ValueError(f"Invalid table or column: {e}") from e
            raise  # Re-raise other operational errors
    return counts
