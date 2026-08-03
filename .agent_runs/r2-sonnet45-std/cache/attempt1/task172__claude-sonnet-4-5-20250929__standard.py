import sqlite3
import re


def group_aggregate(
    conn: sqlite3.Connection,
    table: str,
    group_column: str,
    agg_column: str,
    agg: str = 'SUM'
) -> list[tuple]:
    """
    Run a GROUP BY aggregation query and return results.
    
    Args:
        conn: SQLite database connection
        table: Table name (must be valid identifier)
        group_column: Column to group by (must be valid identifier)
        agg_column: Column to aggregate (must be valid identifier)
        agg: Aggregation function (SUM, AVG, MIN, MAX, COUNT - case insensitive)
    
    Returns:
        List of (group_value, aggregate_value) tuples ordered by group_value ascending
    
    Raises:
        ValueError: If identifiers are invalid or agg function is not whitelisted
    """
    # Validate identifier pattern
    identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    
    if not identifier_pattern.match(table):
        raise ValueError(f"Invalid table identifier: {table}")
    if not identifier_pattern.match(group_column):
        raise ValueError(f"Invalid group_column identifier: {group_column}")
    if not identifier_pattern.match(agg_column):
        raise ValueError(f"Invalid agg_column identifier: {agg_column}")
    
    # Validate aggregation function (case-insensitive whitelist)
    valid_aggs = {'SUM', 'AVG', 'MIN', 'MAX', 'COUNT'}
    agg_upper = agg.upper()
    if agg_upper not in valid_aggs:
        raise ValueError(f"Invalid aggregation function: {agg}")
    
    # Build SQL query with double-quoted identifiers
    query = f'''
        SELECT "{group_column}", {agg_upper}("{agg_column}")
        FROM "{table}"
        GROUP BY "{group_column}"
        ORDER BY "{group_column}" ASC
    '''
    
    # Execute query and fetch results
    cursor = conn.execute(query)
    results = cursor.fetchall()
    
    return results
