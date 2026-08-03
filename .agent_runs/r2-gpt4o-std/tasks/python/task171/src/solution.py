import sqlite3
import re
from typing import Collection, List, Tuple, Optional

def fetch_sorted(
    conn: sqlite3.Connection,
    table: str,
    sort_column: str,
    allowed_columns: Collection[str],
    descending: bool = False,
    limit: Optional[int] = None
) -> List[Tuple]:
    # Validate table and sort_column as identifiers
    identifier_pattern = r"^[A-Za-z_][A-Za-z0-9_]*$"
    if not re.match(identifier_pattern, table):
        raise ValueError(f"Invalid table identifier: {table}")
    if not re.match(identifier_pattern, sort_column):
        raise ValueError(f"Invalid sort column identifier: {sort_column}")

    # Check if sort_column is in allowed_columns
    if sort_column not in allowed_columns:
        raise ValueError(f"Sort column '{sort_column}' is not allowed.")

    # Validate limit
    if limit is not None:
        if not isinstance(limit, int) or limit < 0:
            raise ValueError("Limit must be a non-negative integer or None.")

    # Build the SQL query
    order_direction = "DESC" if descending else "ASC"
    query = f'SELECT * FROM "{table}" ORDER BY "{sort_column}" {order_direction}, rowid ASC'
    params = []

    if limit is not None:
        query += " LIMIT ?"
        params.append(limit)

    # Execute the query and fetch results
    cursor = conn.execute(query, params)
    rows = cursor.fetchall()
    return rows
