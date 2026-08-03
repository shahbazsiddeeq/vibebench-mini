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
        ValueError: If table, key_column, or any SET column name is an invalid identifier,
                    if rows is not a list, if a dict in rows is missing key_column,
                    or if a dict in rows has no other columns to set.
    """
    if not isinstance(rows, list):
        raise ValueError("rows must be a list")

    if not rows:
        return 0

    validated_table = _validate_identifier(table)
    validated_key_column = _validate_identifier(key_column)

    total_rows_modified = 0
    cursor = conn.cursor()

    try:
        for row_data in rows:
            if key_column not in row_data:
                raise ValueError(f"Each row dictionary must contain the key_column '{key_column}'")

            set_clauses = []
            set_values = []
            
            # Collect columns to update, excluding the key_column
            update_columns = {k: v for k, v in row_data.items() if k != key_column}

            if not update_columns:
                raise ValueError("Each row dictionary must contain at least one column to set besides the key_column")

            for col, value in update_columns.items():
                validated_col = _validate_identifier(col)
                set_clauses.append(f"{validated_col} = ?")
                set_values.append(value)

            if not set_clauses:
                # This case should ideally be caught by the check above, but as a safeguard
                continue

            set_sql = ", ".join(set_clauses)
            
            # The key_column value for the WHERE clause
            where_value = row_data[key_column]
            
            sql = f"UPDATE {validated_table} SET {set_sql} WHERE {validated_key_column} = ?"
            
            # Combine SET values with the WHERE value
            params = set_values + [where_value]

            cursor.execute(sql, params)
            total_rows_modified += cursor.rowcount
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()

    return total_rows_modified
