import sqlite3
import re

def _validate_identifier(identifier: str, name: str):
    """Validates if the identifier matches the SQL identifier pattern."""
    if not re.fullmatch(r"^[A-Za-z_][A-Za-z0-9_]*$", identifier):
        raise ValueError(f"Invalid {name} identifier: '{identifier}'")
    return f'"{identifier}"'

def group_aggregate(conn: sqlite3.Connection, table: str, group_column: str, agg_column: str, agg: str = 'SUM') -> list[tuple]:
    """
    Runs SELECT <group_column>, <AGG>(<agg_column>) FROM <table> GROUP BY <group_column>
    and returns a list of (group_value, aggregate_value) tuples ordered by group_value ascending.

    Args:
        conn: An active sqlite3.Connection object.
        table: The name of the table. Must be a valid SQL identifier.
        group_column: The column to group by. Must be a valid SQL identifier.
        agg_column: The column to aggregate. Must be a valid SQL identifier.
        agg: The aggregation function (SUM, AVG, MIN, MAX, COUNT). Case-insensitive.

    Returns:
        A list of (group_value, aggregate_value) tuples.

    Raises:
        ValueError: If any input identifier is invalid or the aggregation function is not allowed.
        sqlite3.Error: For database-related errors.
    """
    allowed_aggs = {"SUM", "AVG", "MIN", "MAX", "COUNT"}
    agg_upper = agg.upper()

    if agg_upper not in allowed_aggs:
        raise ValueError(f"Invalid aggregation function: '{agg}'. Allowed functions are {', '.join(allowed_aggs)}.")

    try:
        sanitized_table = _validate_identifier(table, "table")
        sanitized_group_column = _validate_identifier(group_column, "group_column")
        sanitized_agg_column = _validate_identifier(agg_column, "agg_column")
    except ValueError as e:
        raise e

    # Construct the SQL query using validated and double-quoted identifiers.
    # No user input is directly formatted into the SQL string.
    query = (
        f"SELECT {sanitized_group_column}, {agg_upper}({sanitized_agg_column}) "
        f"FROM {sanitized_table} "
        f"GROUP BY {sanitized_group_column} "
        f"ORDER BY {sanitized_group_column} ASC"
    )

    try:
        cursor = conn.execute(query)
        return cursor.fetchall()
    except sqlite3.Error as e:
        # Re-raise database errors to avoid exposing internal details directly
        # but still indicate a database issue.
        raise sqlite3.Error(f"Database error during aggregation: {e}") from e
