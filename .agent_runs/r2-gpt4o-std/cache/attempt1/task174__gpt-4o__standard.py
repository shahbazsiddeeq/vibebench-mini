import sqlite3
import re

def bulk_update(conn: sqlite3.Connection, table: str, key_column: str, rows: list[dict]) -> int:
    # Validate identifiers
    identifier_pattern = r'^[A-Za-z_][A-Za-z0-9_]*$'
    if not re.match(identifier_pattern, table):
        raise ValueError("Invalid table name")
    if not re.match(identifier_pattern, key_column):
        raise ValueError("Invalid key column name")

    if not isinstance(rows, list):
        raise ValueError("Rows must be a list")

    if not rows:
        return 0

    total_modified = 0

    try:
        with conn:
            for row in rows:
                if key_column not in row:
                    raise ValueError("Each row must contain the key column")
                
                # Extract columns to update
                columns = [col for col in row if col != key_column]
                if not columns:
                    raise ValueError("Each row must have at least one column to update")

                # Validate column names
                for col in columns:
                    if not re.match(identifier_pattern, col):
                        raise ValueError(f"Invalid column name: {col}")

                # Prepare SQL statement
                set_clause = ", ".join(f'"{col}" = ?' for col in columns)
                sql = f'UPDATE "{table}" SET {set_clause} WHERE "{key_column}" = ?'

                # Prepare values
                values = [row[col] for col in columns] + [row[key_column]]

                # Execute the update
                cursor = conn.execute(sql, values)
                total_modified += cursor.rowcount

    except sqlite3.Error as e:
        raise e

    return total_modified
