import sqlite3
import re

def transfer(conn: sqlite3.Connection, table: str, id_column: str, balance_column: str, from_id, to_id, amount: int) -> tuple[int, int]:
    # Validate identifiers
    identifier_pattern = r'^[A-Za-z_][A-Za-z0-9_]*$'
    if not re.match(identifier_pattern, table) or not re.match(identifier_pattern, id_column) or not re.match(identifier_pattern, balance_column):
        raise ValueError("Invalid SQL identifier")

    # Validate amount
    if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
        raise ValueError("Amount must be a positive integer")

    # Validate from_id and to_id
    if from_id == to_id:
        raise ValueError("from_id and to_id must differ")

    # Begin transaction
    with conn:
        # Check if both accounts exist
        cursor = conn.execute(f'SELECT {balance_column} FROM {table} WHERE {id_column} = ?', (from_id,))
        from_row = cursor.fetchone()
        if from_row is None:
            raise ValueError("account not found")

        cursor = conn.execute(f'SELECT {balance_column} FROM {table} WHERE {id_column} = ?', (to_id,))
        to_row = cursor.fetchone()
        if to_row is None:
            raise ValueError("account not found")

        from_balance = from_row[0]
        to_balance = to_row[0]

        # Check if from_account has sufficient funds
        if from_balance < amount:
            raise ValueError("insufficient funds")

        # Perform the transfer
        new_from_balance = from_balance - amount
        new_to_balance = to_balance + amount

        conn.execute(f'UPDATE {table} SET {balance_column} = ? WHERE {id_column} = ?', (new_from_balance, from_id))
        conn.execute(f'UPDATE {table} SET {balance_column} = ? WHERE {id_column} = ?', (new_to_balance, to_id))

        return new_from_balance, new_to_balance
