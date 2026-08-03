import sqlite3
import re

def transfer(conn: sqlite3.Connection, table: str, id_column: str, balance_column: str, from_id, to_id, amount: int) -> tuple[int, int]:
    # Validate identifiers
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', table):
        raise ValueError("Invalid table name")
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', id_column):
        raise ValueError("Invalid id column name")
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', balance_column):
        raise ValueError("Invalid balance column name")

    # Validate amount
    if not isinstance(amount, int) or amount <= 0:
        raise ValueError("Amount must be a positive integer")
    
    if from_id == to_id:
        raise ValueError("from_id and to_id must differ")

    # Start transaction
    cursor = conn.cursor()
    try:
        # Check if accounts exist
        cursor.execute(f"SELECT {balance_column} FROM {table} WHERE {id_column} = ?", (from_id,))
        from_balance_row = cursor.fetchone()
        if from_balance_row is None:
            raise ValueError("account not found")
        from_balance = from_balance_row[0]

        cursor.execute(f"SELECT {balance_column} FROM {table} WHERE {id_column} = ?", (to_id,))
        to_balance_row = cursor.fetchone()
        if to_balance_row is None:
            raise ValueError("account not found")
        to_balance = to_balance_row[0]

        # Check if sufficient funds
        if from_balance < amount:
            raise ValueError("insufficient funds")

        # Perform the transfer
        new_from_balance = from_balance - amount
        new_to_balance = to_balance + amount

        cursor.execute(f"UPDATE {table} SET {balance_column} = ? WHERE {id_column} = ?", (new_from_balance, from_id))
        cursor.execute(f"UPDATE {table} SET {balance_column} = ? WHERE {id_column} = ?", (new_to_balance, to_id))

        # Commit the transaction
        conn.commit()

        return new_from_balance, new_to_balance

    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
