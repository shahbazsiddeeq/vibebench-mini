import sqlite3
import re

def _validate_identifier(identifier: str):
    """Validates if the identifier matches the allowed pattern."""
    if not re.fullmatch(r"^[A-Za-z_][A-Za-z0-9_]*$", identifier):
        raise ValueError(f"Invalid identifier: {identifier}")
    return f'"{identifier}"'

def transfer(conn: sqlite3.Connection, table: str, id_column: str, balance_column: str, from_id, to_id, amount: int) -> tuple[int, int]:
    """
    Atomically moves `amount` from the row whose id_column == from_id to the row
    whose id_column == to_id within a single transaction, and returns
    (new_from_balance, new_to_balance).

    All VALUES (from_id, to_id, amount) are passed as bound parameters.
    table, id_column and balance_column are IDENTIFIERS validated against
    ^[A-Za-z_][A-Za-z0-9_]*$ and double-quoted into the SQL (ValueError otherwise).

    Rules, each checked before any write:
    - amount must be an int (not bool) and > 0 else ValueError;
    - from_id and to_id must differ else ValueError;
    - both rows must exist else ValueError('account not found');
    - the source balance must be >= amount else ValueError('insufficient funds').

    On ANY failure after starting, the transaction is rolled back so balances are
    unchanged; on success it is committed.
    """

    # 1. Validate identifiers
    quoted_table = _validate_identifier(table)
    quoted_id_column = _validate_identifier(id_column)
    quoted_balance_column = _validate_identifier(balance_column)

    # 2. Validate amount
    if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
        raise ValueError("Amount must be an integer greater than 0.")

    # 3. Validate from_id and to_id
    if from_id == to_id:
        raise ValueError("Source and destination accounts cannot be the same.")

    with conn:  # Use connection as a context manager for atomic transactions
        # Check if accounts exist and get initial balances
        select_sql = f"SELECT {quoted_balance_column} FROM {quoted_table} WHERE {quoted_id_column} = ?"
        
        cursor = conn.execute(select_sql, (from_id,))
        from_balance_row = cursor.fetchone()
        
        cursor = conn.execute(select_sql, (to_id,))
        to_balance_row = cursor.fetchone()

        if from_balance_row is None or to_balance_row is None:
            raise ValueError("account not found")

        from_balance = from_balance_row[0]
        to_balance = to_balance_row[0]

        # Check for insufficient funds
        if from_balance < amount:
            raise ValueError("insufficient funds")

        # Perform the updates
        update_from_sql = f"UPDATE {quoted_table} SET {quoted_balance_column} = {quoted_balance_column} - ? WHERE {quoted_id_column} = ?"
        conn.execute(update_from_sql, (amount, from_id))

        update_to_sql = f"UPDATE {quoted_table} SET {quoted_balance_column} = {quoted_balance_column} + ? WHERE {quoted_id_column} = ?"
        conn.execute(update_to_sql, (amount, to_id))

        # Get new balances to return
        cursor = conn.execute(select_sql, (from_id,))
        new_from_balance = cursor.fetchone()[0]

        cursor = conn.execute(select_sql, (to_id,))
        new_to_balance = cursor.fetchone()[0]

    return new_from_balance, new_to_balance
