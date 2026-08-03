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
            if len(row) < 2:
                raise ValueError("At least one column must be updated.")

            key_value = row[key_column]
            set_columns = {k: v for k, v in row.items() if k != key_column}
            set_statements = []
            values = []

            for col, value in set_columns.items():
                col = validate_identifier(col)
                set_statements.append(f"{col} = ?")
                values.append(value)

            set_clause = ", ".join(set_statements)
            sql = f"UPDATE {table} SET {set_clause} WHERE {key_column} = ?"
            values.append(key_value)

            cursor = conn.execute(sql, values)
            total_modified += cursor.rowcount

    return total_modified
