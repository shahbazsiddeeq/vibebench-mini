import sqlite3
import re


def group_aggregate(
    conn: sqlite3.Connection,
    table: str,
    group_column: str,
    agg_column: str,
    agg: str = "SUM",
) -> list[tuple]:
    """
    Run a GROUP BY aggregation query and return results as a list of tuples.
    
    Args:
        conn: SQLite connection
        table: Table name (identifier)
        group_column: Column to group by (identifier)
        agg_column: Column to aggregate (identifier)
        agg: Aggregation function (SUM, AVG, MIN, MAX, COUNT) - case-insensitive
    
    Returns:
        List of (group_value, aggregate_value) tuples ordered by group_value ascending
        with NULL values first
    
    Raises:
        ValueError: If agg is not a valid function or identifiers don't match pattern
    """
    # Validate aggregation function (whitelist)
    valid_aggs = {"SUM", "AVG", "MIN", "MAX", "COUNT"}
    agg_upper = agg.upper()
    if agg_upper not in valid_aggs:
        raise ValueError(f"Invalid aggregation function: {agg}")
    
    # Validate identifiers - must match ^[A-Za-z_][A-Za-z0-9_]*$
    identifier_pattern = r"^[A-Za-z_][A-Za-z0-9_]*$"
    
    for identifier, name in [
        (table, "table"),
        (group_column, "group_column"),
        (agg_column, "agg_column"),
    ]:
        if not re.match(identifier_pattern, identifier):
            raise ValueError(f"Invalid identifier: {name}")
    
    # Build SQL query with double-quoted identifiers
    sql = f'SELECT "{group_column}", {agg_upper}("{agg_column}") FROM "{table}" GROUP BY "{group_column}" ORDER BY "{group_column}"'
    
    # Execute query and fetch results
    cursor = conn.execute(sql)
    results = cursor.fetchall()
    
    return results
