# src/solution.py

import sqlite3
import re

def validate_identifier(identifier: str) -> str:
    """Validate and sanitize SQL identifiers."""
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', identifier):
        raise ValueError("Invalid identifier")
    return f'"{identifier}"'

def transfer(conn: sqlite3.Connection, table: str, id_column: str, balance_column: str, from_id: int, to_id: int, amount: int) -> tuple[int, int]:
    """Atomically transfer amount from one account to another."""
    
    # Validate inputs
    if not isinstance(amount, int) or amount <= 0:
        raise ValueError("Amount must be a positive integer")
    if from_id == to_id:
        raise ValueError("from_id and to_id must differ")

    # Sanitize identifiers
    table = validate_identifier(table)
    id_column = validate_identifier(id_column)
    balance_column = validate_identifier(balance_column)

    # Start transaction
    cursor = conn.cursor()
    try:
        # Check if both accounts exist and get their balances
        cursor.execute(f"SELECT {balance_column} FROM {table} WHERE {id_column} = ?", (from_id,))
        from_balance = cursor.fetchone()
        if from_balance is None:
            raise ValueError("account not found")
        from_balance = from_balance[0]

        cursor.execute(f"SELECT {balance_column} FROM {table} WHERE {id_column} = ?", (to_id,))
        to_balance = cursor.fetchone()
        if to_balance is None:
            raise ValueError("account not found")
        to_balance = to_balance[0]

        # Check if sufficient funds are available
        if from_balance < amount:
            raise ValueError("insufficient funds")

        # Perform the transfer
        cursor.execute(f"UPDATE {table} SET {balance_column} = {balance_column} - ? WHERE {id_column} = ?", (amount, from_id))
        cursor.execute(f"UPDATE {table} SET {balance_column} = {balance_column} + ? WHERE {id_column} = ?", (amount, to_id))

        # Commit the transaction
        conn.commit()

        # Return new balances
        return (from_balance - amount, to_balance + amount)

    except Exception:
        # Rollback on any failure
        conn.rollback()
        raise
    finally:
        cursor.close()
