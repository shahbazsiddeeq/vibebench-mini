import sqlite3
import re
from typing import Collection


def fetch_sorted(
    conn: sqlite3.Connection,
    table: str,
    sort_column: str,
    allowed_columns: Collection[str],
    descending: bool = False,
    limit: int | None = None
) -> list[tuple]:
    """
    Fetch rows from a table sorted by a specified column.
    
    Args:
        conn: SQLite database connection
        table: Table name (must be valid identifier)
        sort_column: Column to sort by (must be valid identifier and in allowed_columns)
        allowed_columns: Whitelist of allowed column names
        descending: If True, sort descending; otherwise ascending
        limit: Optional limit on number of rows (must be non-negative int)
    
    Returns:
        List of tuples representing rows
    
    Raises:
        ValueError: If validation fails
    """
    # Identifier regex pattern
    identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    
    # Validate table name
    if not identifier_pattern.match(table):
        raise ValueError(f"Invalid table identifier: {table}")
    
    # Validate sort_column name
    if not identifier_pattern.match(sort_column):
        raise ValueError(f"Invalid sort_column identifier: {sort_column}")
    
    # Check if sort_column is in allowed_columns
    if sort_column not in allowed_columns:
        raise ValueError(f"sort_column '{sort_column}' not in allowed_columns")
    
    # Validate limit if provided
    if limit is not None:
        if not isinstance(limit, int) or isinstance(limit, bool):
            raise ValueError(f"limit must be an int or None, got {type(limit)}")
        if limit < 0:
            raise ValueError(f"limit must be non-negative, got {limit}")
    
    # Build the SQL query
    # Use double quotes for identifiers
    sort_direction = "DESC" if descending else "ASC"
    
    # Build base query with ORDER BY
    query = f'SELECT * FROM "{table}" ORDER BY "{sort_column}" {sort_direction}, rowid ASC'
    
    # Add LIMIT if specified
    params = []
    if limit is not None:
        query += " LIMIT ?"
        params.append(limit)
    
    # Execute query
    cursor = conn.execute(query, params)
    rows = cursor.fetchall()
    
    return rows
