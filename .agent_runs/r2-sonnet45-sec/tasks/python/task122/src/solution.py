import sqlite3
import re


def value_counts(db_path, table, column):
    """
    Returns a dict mapping each distinct value in the given column to its count.
    
    Args:
        db_path: Path to the SQLite database file
        table: Name of the table
        column: Name of the column
        
    Returns:
        Dict mapping distinct values to their counts
        
    Raises:
        ValueError: If table or column is an invalid identifier
    """
    # Validate identifiers (table and column names)
    # SQLite identifiers can contain letters, digits, underscores, and dollar signs
    # They cannot start with a digit (unless quoted, but we don't allow that for security)
    # We use a strict pattern to prevent SQL injection
    identifier_pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
    
    if not identifier_pattern.match(table):
        raise ValueError(f"Invalid table identifier: {table}")
    
    if not identifier_pattern.match(column):
        raise ValueError(f"Invalid column identifier: {column}")
    
    # Connect to database and execute query
    try:
        with sqlite3.connect(db_path) as conn:
            # Use parameterized identifiers by validating them first
            # Since we've validated the identifiers, it's safe to use string formatting
            # Note: SQLite doesn't support parameterized table/column names with ?
            query = f"SELECT {column}, COUNT(*) FROM {table} GROUP BY {column}"
            
            cursor = conn.execute(query)
            results = cursor.fetchall()
            
            # Build the result dictionary
            result_dict = {}
            for value, count in results:
                result_dict[value] = count
            
            return result_dict
            
    except sqlite3.OperationalError as e:
        # This could happen if table or column doesn't exist
        # Re-raise as a more generic error without exposing internals
        raise ValueError(f"Database operation failed") from None
    except sqlite3.Error as e:
        # Catch other database errors
        raise ValueError(f"Database error occurred") from None
