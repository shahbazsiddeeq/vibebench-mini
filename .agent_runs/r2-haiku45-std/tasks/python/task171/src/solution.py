import sqlite3
import re
from typing import Collection, Optional


def fetch_sorted(
    conn: sqlite3.Connection,
    table: str,
    sort_column: str,
    allowed_columns: Collection[str],
    descending: bool = False,
    limit: Optional[int] = None,
) -> list[tuple]:
    """
    Fetch rows from a table sorted by a specified column.
    
    Args:
        conn: SQLite connection
        table: Table name (must match identifier pattern)
        sort_column: Column to sort by (must be in allowed_columns and match identifier pattern)
        allowed_columns: Whitelist of allowed columns for sorting
        descending: If True, sort DESC; if False, sort ASC
        limit: Optional non-negative integer limit on results
    
    Returns:
        List of tuples representing rows in the table's definition order
    
    Raises:
        ValueError: If identifiers are invalid, sort_column not in allowed_columns, or limit is invalid
    """
    
    # Validate identifier pattern: ^[A-Za-z_][A-Za-z0-9_]*$
    identifier_pattern = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
    
    # Validate table identifier
    if not identifier_pattern.match(table):
        raise ValueError(f"Invalid table identifier: {table}")
    
    # Validate sort_column identifier
    if not identifier_pattern.match(sort_column):
        raise ValueError(f"Invalid sort column identifier: {sort_column}")
    
    # Check that sort_column is in allowed_columns (whitelist check)
    if sort_column not in allowed_columns:
        raise ValueError(f"Sort column '{sort_column}' not in allowed columns")
    
    # Validate limit parameter
    if limit is not None:
        if not isinstance(limit, int) or isinstance(limit, bool):
            raise ValueError(f"Limit must be a non-negative integer, got {type(limit)}")
        if limit < 0:
            raise ValueError(f"Limit must be non-negative, got {limit}")
    
    # Build the SQL query with double-quoted identifiers
    sort_direction = "DESC" if descending else "ASC"
    query = f'SELECT * FROM "{table}" ORDER BY "{sort_column}" {sort_direction}, rowid ASC'
    
    # Add LIMIT clause if specified
    if limit is not None:
        query += " LIMIT ?"
        rows = conn.execute(query, (limit,)).fetchall()
    else:
        rows = conn.execute(query).fetchall()
    
    return rows
