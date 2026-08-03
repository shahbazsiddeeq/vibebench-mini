# src/solution.py

import sqlite3
import re
from typing import List, Tuple, Collection, Optional

def fetch_sorted(
    conn: sqlite3.Connection,
    table: str,
    sort_column: str,
    allowed_columns: Collection[str],
    descending: bool = False,
    limit: Optional[int] = None
) -> List[Tuple]:
    # Validate table and sort_column identifiers
    identifier_regex = r'^[A-Za-z_][A-Za-z0-9_]*$'
    
    if not re.match(identifier_regex, table):
        raise ValueError("Invalid table identifier.")
    
    if sort_column not in allowed_columns:
        raise ValueError("sort_column must be in allowed_columns.")
    
    if not re.match(identifier_regex, sort_column):
        raise ValueError("Invalid sort_column identifier.")
    
    # Validate limit
    if limit is not None:
        if not isinstance(limit, int) or limit < 0:
            raise ValueError("limit must be a non-negative integer.")
    
    # Construct the SQL query
    order_direction = "DESC" if descending else "ASC"
    limit_clause = f"LIMIT ?" if limit is not None else ""
    
    query = f'SELECT * FROM "{table}" ORDER BY "{sort_column}" {order_direction} {limit_clause}'.strip()
    
    # Execute the query
    cursor = conn.cursor()
    if limit is not None:
        cursor.execute(query, (limit,))
    else:
        cursor.execute(query)
    
    # Fetch and return the results
    rows = cursor.fetchall()
    return rows
