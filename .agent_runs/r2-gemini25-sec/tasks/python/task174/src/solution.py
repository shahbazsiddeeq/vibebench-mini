import sqlite3
import re

def _validate_identifier(identifier: str):
    """Validates if the identifier matches the SQL identifier pattern."""
    if not re.fullmatch(r"^[A-Za-z_][A-Za-z0-9_]*$", identifier):
        raise ValueError(f"Invalid SQL identifier: {identifier}")
    return f'"{identifier}"'

def bulk_update(conn: sqlite3.Connection, table: str, key_column: str, rows: list[dict]) -> int:
    """
    Applies bulk updates to a table within a single transaction.

    Args:
        conn: The SQLite connection object.
        table: The name of the table to update.
        key_column: The name of the key column used for WHERE clauses.
        rows: A list of dictionaries, where each dictionary represents a row to update.
              Each dict must contain key_column and at least one other column to set.

    Returns:
        The total number of rows modified.

    Raises:
        ValueError: If inputs are invalid (e.g., malformed identifiers,
                    missing key_column in a row, empty update dicts,
                    or `rows` is not a list).
        sqlite3.Error: If any database operation fails.
    """
    if not isinstance(rows, list):
        raise ValueError("`rows` must be a list.")

    if not rows:
        return 0

    validated_table = _validate_identifier(table)
    validated_key_column = _validate_identifier(key_column)

    total_rows_modified = 0
    with conn:  # This handles transaction management (commit/rollback)
        for row_data in rows:
            if not isinstance(row_data, dict):
                raise ValueError("Each item in `rows` must be a dictionary.")

            if key_column not in row_data:
                raise ValueError(f"Each row dictionary must contain the key_column: '{key_column}'")

            set_clauses = []
            params = []
            update_key_value = row_data[key_column]

            for col, value in row_data.items():
                if col == key_column:
                    continue

                validated_col = _validate_identifier(col)
                set_clauses.append(f"{validated_col} = ?")
                params.append(value)

            if not set_clauses:
                raise ValueError(f"Each row dictionary must contain at least one column to set besides '{key_column}'.")

            params.append(update_key_value)

            sql = f"UPDATE {validated_table} SET {', '.join(set_clauses)} WHERE {validated_key_column} = ?"

            cursor = conn.execute(sql, params)
            total_rows_modified += cursor.rowcount

    return total_rows_modified
