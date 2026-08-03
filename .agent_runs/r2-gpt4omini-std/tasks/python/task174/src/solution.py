import sqlite3
import re

def bulk_update(conn: sqlite3.Connection, table: str, key_column: str, rows: list[dict]) -> int:
    # Validate identifiers
    def validate_identifier(identifier: str) -> None:
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', identifier):
            raise ValueError(f"Invalid identifier: {identifier}")

    validate_identifier(table)
    validate_identifier(key_column)

    if not isinstance(rows, list):
        raise ValueError("Rows must be a list.")
    
    if not rows:
        return 0

    total_modified = 0
    with conn:
        for row in rows:
            if key_column not in row:
                raise ValueError(f"Missing key column: {key_column}")
            if len(row) == 1:
                raise ValueError("At least one column must be updated.")

            # Prepare the SQL statement
            set_clause = []
            values = []
            for col, value in row.items():
                if col == key_column:
                    continue
                validate_identifier(col)
                set_clause.append(f'"{col}" = ?')
                values.append(value)

            set_clause_str = ", ".join(set_clause)
            values.append(row[key_column])
            sql = f'UPDATE "{table}" SET {set_clause_str} WHERE "{key_column}" = ?'

            cursor = conn.execute(sql, values)
            total_modified += cursor.rowcount

    return total_modified
