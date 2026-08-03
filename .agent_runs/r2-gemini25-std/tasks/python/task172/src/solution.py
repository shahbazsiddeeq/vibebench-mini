import sqlite3
import re

def group_aggregate(conn: sqlite3.Connection, table: str, group_column: str, agg_column: str, agg: str = 'SUM') -> list[tuple]:
    """
    Runs SELECT <group_column>, <AGG>(<agg_column>) FROM <table> GROUP BY <group_column>
    and returns a list of (group_value, aggregate_value) tuples ordered by group_value
    ascending with SQLite's default NULL-first ordering.

    Args:
        conn: An active sqlite3.Connection object.
        table: The name of the table.
        group_column: The column to group by.
        agg_column: The column to aggregate.
        agg: The aggregation function (SUM, AVG, MIN, MAX, COUNT). Case-insensitive.

    Returns:
        A list of (group_value, aggregate_value) tuples.

    Raises:
        ValueError: If agg is not one of the allowed functions, or if table,
                    group_column, or agg_column are not valid identifiers.
    """

    allowed_aggs = {'SUM', 'AVG', 'MIN', 'MAX', 'COUNT'}
    agg_upper = agg.upper()

    if agg_upper not in allowed_aggs:
        raise ValueError(f"Invalid aggregation function: {agg}. Must be one of {', '.join(allowed_aggs)}")

    identifier_pattern = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

    for identifier in [table, group_column, agg_column]:
        if not identifier_pattern.match(identifier):
            raise ValueError(f"Invalid identifier: {identifier}. Must match pattern ^[A-Za-z_][A-Za-z0-9_]*$")

    # Double-quote identifiers to handle potential keywords or special characters
    # (though the regex already restricts them to safe names, this is good practice)
    quoted_table = f'"{table}"'
    quoted_group_column = f'"{group_column}"'
    quoted_agg_column = f'"{agg_column}"'

    query = f"SELECT {quoted_group_column}, {agg_upper}({quoted_agg_column}) FROM {quoted_table} GROUP BY {quoted_group_column} ORDER BY {quoted_group_column} ASC"

    cursor = conn.execute(query)
    return cursor.fetchall()
