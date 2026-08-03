import sqlite3
import re

def _validate_identifier(identifier: str, name: str):
    """Validates if the identifier matches the allowed pattern."""
    if not re.fullmatch(r"^[A-Za-z_][A-Za-z0-9_]*$", identifier):
        raise ValueError(f"Invalid {name} identifier: {identifier}")
    return f'"{identifier}"'

def transfer(conn: sqlite3.Connection, table: str, id_column: str, balance_column: str, from_id, to_id, amount: int) -> tuple[int, int]:
    """
    Atomically moves `amount` from the row whose id_column == from_id to the row
    whose id_column == to_id within a single transaction.

    Args:
        conn: The SQLite database connection.
        table: The name of the table.
        id_column: The name of the ID column.
        balance_column: The name of the balance column.
        from_id: The ID of the source account.
        to_id: The ID of the destination account.
        amount: The amount to transfer.

    Returns:
        A tuple (new_from_balance, new_to_balance) after the transfer.

    Raises:
        ValueError: If any input validation fails or transfer conditions are not met.
    """

    # 1. Validate identifiers
    quoted_table = _validate_identifier(table, "table")
    quoted_id_column = _validate_identifier(id_column, "id_column")
    quoted_balance_column = _validate_identifier(balance_column, "balance_column")

    # 2. Validate amount
    if not isinstance(amount, int) or isinstance(amount, bool):
        raise ValueError("Amount must be an integer (not boolean).")
    if amount <= 0:
        raise ValueError("Amount must be greater than 0.")

    # 3. Validate from_id and to_id
    if from_id == to_id:
        raise ValueError("Source and destination accounts must be different.")

    with conn:  # Use connection as a context manager for atomic transactions
        # 4. Check if both rows exist and get current balances
        select_sql = f"SELECT {quoted_balance_column} FROM {quoted_table} WHERE {quoted_id_column} = ?"
        
        cursor = conn.execute(select_sql, (from_id,))
        from_balance_row = cursor.fetchone()
        
        cursor = conn.execute(select_sql, (to_id,))
        to_balance_row = cursor.fetchone()

        if from_balance_row is None or to_balance_row is None:
            raise ValueError("account not found")

        current_from_balance = from_balance_row[0]
        current_to_balance = to_balance_row[0]

        # 5. Check for insufficient funds
        if current_from_balance < amount:
            raise ValueError("insufficient funds")

        # 6. Perform the transfer
        new_from_balance = current_from_balance - amount
        new_to_balance = current_to_balance + amount

        update_sql = f"UPDATE {quoted_table} SET {quoted_balance_column} = ? WHERE {quoted_id_column} = ?"
        
        conn.execute(update_sql, (new_from_balance, from_id))
        conn.execute(update_sql, (new_to_balance, to_id))

    return new_from_balance, new_to_balance
