import sqlite3
import re

def validate_identifier(identifier: str) -> str:
    """Validate and sanitize SQL identifiers."""
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', identifier):
        raise ValueError(f"Invalid identifier: {identifier}")
    return f'"{identifier}"'

def bulk_update(conn: sqlite3.Connection, table: str, key_column: str, rows: list[dict]) -> int:
    """Bulk update rows in a specified SQLite table."""
    if not isinstance(rows, list):
        raise ValueError("Rows must be a list.")
    
    if not rows:
        return 0

    table = validate_identifier(table)
    key_column = validate_identifier(key_column)

    total_modified = 0

    with conn:
        for row in rows:
            if key_column not in row:
                raise ValueError(f"Missing key column: {key_column}")
            if len(row) < 2:  # Must have at least one other column to update
                raise ValueError("Each row must contain at least one column to update.")

            # Prepare the SET clause and values
            set_clause = []
            values = []
            for col, value in row.items():
                if col == key_column:
                    continue
                set_clause.append(f"{validate_identifier(col)} = ?")
                values.append(value)

            # Construct the SQL statement
            sql = f"UPDATE {table} SET {', '.join(set_clause)} WHERE {key_column} = ?"
            values.append(row[key_column])  # Add the key column value for the WHERE clause

            # Execute the update
            cursor = conn.execute(sql, values)
            total_modified += cursor.rowcount

    return total_modified
