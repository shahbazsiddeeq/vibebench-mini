import sqlite3
import re
from typing import Collection


def fetch_sorted(
    conn: sqlite3.Connection,
    table: str,
    sort_column: str,
    allowed_columns: Collection[str],
    descending: bool = False,
    limit: int | None = None,
) -> list[tuple]:
    """
    Fetch sorted rows from a table with security validations.
    
    Args:
        conn: SQLite database connection
        table: Table name (must be valid identifier)
        sort_column: Column to sort by (must be in allowed_columns and valid identifier)
        allowed_columns: Whitelist of allowed column names
        descending: If True, sort DESC; otherwise ASC
        limit: Optional row limit (must be non-negative int if provided)
    
    Returns:
        List of tuples representing rows
    
    Raises:
        ValueError: If validation fails
    """
    # Identifier pattern: must start with letter or underscore, followed by letters, digits, or underscores
    identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    
    # Validate table name
    if not isinstance(table, str) or not identifier_pattern.match(table):
        raise ValueError("Invalid table identifier")
    
    # Validate sort_column name
    if not isinstance(sort_column, str) or not identifier_pattern.match(sort_column):
        raise ValueError("Invalid sort_column identifier")
    
    # Check sort_column is in whitelist
    if sort_column not in allowed_columns:
        raise ValueError("sort_column not in allowed_columns")
    
    # Validate descending is boolean
    if not isinstance(descending, bool):
        raise ValueError("descending must be a boolean")
    
    # Validate limit
    if limit is not None:
        if not isinstance(limit, int) or isinstance(limit, bool):
            raise ValueError("limit must be an integer or None")
        if limit < 0:
            raise ValueError("limit must be non-negative")
    
    # Build SQL query
    # Use double quotes for identifiers (table and column names)
    sort_direction = "DESC" if descending else "ASC"
    
    # Build base query with double-quoted identifiers
    query = f'SELECT * FROM "{table}" ORDER BY "{sort_column}" {sort_direction}, rowid ASC'
    
    # Add LIMIT clause if specified
    params = []
    if limit is not None:
        query += " LIMIT ?"
        params.append(limit)
    
    # Execute query
    cursor = conn.execute(query, params)
    rows = cursor.fetchall()
    
    return rows
