import sqlite3
import re
from typing import List, Tuple, Union


def group_aggregate(
    conn: sqlite3.Connection,
    table: str,
    group_column: str,
    agg_column: str,
    agg: str = "SUM",
) -> List[Tuple[Union[str, None], Union[int, float]]]:
    """
    Run a GROUP BY aggregation query on a SQLite table.
    
    Args:
        conn: SQLite connection object
        table: Table name (identifier)
        group_column: Column to group by (identifier)
        agg_column: Column to aggregate (identifier)
        agg: Aggregation function (SUM, AVG, MIN, MAX, COUNT) - case-insensitive
    
    Returns:
        List of (group_value, aggregate_value) tuples ordered by group_value ascending
        with NULL values first
    
    Raises:
        ValueError: If agg is not in the whitelist or if identifiers are invalid
    """
    # Validate and normalize aggregation function (whitelist)
    valid_aggs = {"SUM", "AVG", "MIN", "MAX", "COUNT"}
    agg_upper = agg.upper()
    if agg_upper not in valid_aggs:
        raise ValueError(
            f"Invalid aggregation function: {agg}. Must be one of {valid_aggs}"
        )
    
    # Validate identifiers - must match ^[A-Za-z_][A-Za-z0-9_]*$
    identifier_pattern = r"^[A-Za-z_][A-Za-z0-9_]*$"
    
    for identifier, name in [
        (table, "table"),
        (group_column, "group_column"),
        (agg_column, "agg_column"),
    ]:
        if not re.match(identifier_pattern, identifier):
            raise ValueError(
                f"Invalid {name} identifier: {identifier}. "
                f"Must match pattern ^[A-Za-z_][A-Za-z0-9_]*$"
            )
    
    # Build the SQL query with double-quoted identifiers
    sql = (
        f'SELECT "{group_column}", {agg_upper}("{agg_column}") '
        f'FROM "{table}" '
        f'GROUP BY "{group_column}" '
        f'ORDER BY "{group_column}" ASC'
    )
    
    # Execute the query
    cursor = conn.execute(sql)
    results = cursor.fetchall()
    
    return results
