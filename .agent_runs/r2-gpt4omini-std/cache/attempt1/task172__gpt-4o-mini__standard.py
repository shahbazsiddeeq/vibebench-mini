import sqlite3
import re

def group_aggregate(conn: sqlite3.Connection, table: str, group_column: str, agg_column: str, agg: str = 'SUM') -> list[tuple]:
    # Validate aggregate function
    valid_aggs = {'SUM', 'AVG', 'MIN', 'MAX', 'COUNT'}
    if agg.upper() not in valid_aggs:
        raise ValueError(f"Invalid aggregate function: {agg}")

    # Validate identifiers
    identifier_pattern = r'^[A-Za-z_][A-Za-z0-9_]*$'
    for identifier in (table, group_column, agg_column):
        if not re.match(identifier_pattern, identifier):
            raise ValueError(f"Invalid identifier: {identifier}")

    # Prepare SQL query
    query = f'SELECT "{group_column}", {agg.upper()}("{agg_column}") FROM "{table}" GROUP BY "{group_column}" ORDER BY "{group_column}"'
    
    # Execute query and fetch results
    cursor = conn.execute(query)
    results = cursor.fetchall()
    
    return results
