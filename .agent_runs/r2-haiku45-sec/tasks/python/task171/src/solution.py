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
    Safely fetch sorted rows from a table with SQL injection protection.
    
    Args:
        conn: SQLite connection
        table: Table name (validated as identifier)
        sort_column: Column to sort by (must be in allowed_columns)
        allowed_columns: Whitelist of allowed columns for sorting
        descending: If True, sort DESC; if False, sort ASC
        limit: Optional non-negative integer limit on results
        
    Returns:
        List of tuples representing rows in the table's definition order
        
    Raises:
        ValueError: If validation fails (invalid identifiers, column not allowed, bad limit)
    """
    
    # Validate identifier pattern: must start with letter or underscore,
    # followed by letters, digits, or underscores
    identifier_pattern = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
    
    # Validate table name
    if not identifier_pattern.match(table):
        raise ValueError(f"Invalid table identifier: {table}")
    
    # Validate sort_column name
    if not identifier_pattern.match(sort_column):
        raise ValueError(f"Invalid sort column identifier: {sort_column}")
    
    # Check that sort_column is in the allowed columns whitelist
    if sort_column not in allowed_columns:
        raise ValueError(f"Sort column '{sort_column}' not in allowed columns")
    
    # Validate limit parameter
    if limit is not None:
        if not isinstance(limit, int) or isinstance(limit, bool):
            raise ValueError(f"Limit must be a non-negative integer, got {type(limit)}")
        if limit < 0:
            raise ValueError(f"Limit must be non-negative, got {limit}")
    
    # Build the SQL query with double-quoted identifiers
    # Double quotes are the standard SQL way to quote identifiers
    sort_direction = "DESC" if descending else "ASC"
    
    query = f'SELECT * FROM "{table}" ORDER BY "{sort_column}" {sort_direction}, rowid ASC'
    
    # Add LIMIT clause if specified
    if limit is not None:
        query += " LIMIT ?"
        params = (limit,)
    else:
        params = ()
    
    # Execute query and fetch results
    cursor = conn.execute(query, params)
    rows = cursor.fetchall()
    
    # Convert to list of tuples (fetchall already returns tuples, but ensure it)
    return [tuple(row) for row in rows]
