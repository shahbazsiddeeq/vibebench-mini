import sqlite3
import re
from typing import Any


def transfer(
    conn: sqlite3.Connection,
    table: str,
    id_column: str,
    balance_column: str,
    from_id: Any,
    to_id: Any,
    amount: int,
) -> tuple[int, int]:
    """
    Atomically transfer amount from one account to another.
    
    Args:
        conn: SQLite connection
        table: Table name (validated as identifier)
        id_column: ID column name (validated as identifier)
        balance_column: Balance column name (validated as identifier)
        from_id: Source account ID
        to_id: Destination account ID
        amount: Amount to transfer (must be positive int, not bool)
    
    Returns:
        Tuple of (new_from_balance, new_to_balance)
    
    Raises:
        ValueError: If validation fails or insufficient funds
    """
    
    # Validate identifiers against ^[A-Za-z_][A-Za-z0-9_]*$
    identifier_pattern = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
    
    for identifier, name in [
        (table, "table"),
        (id_column, "id_column"),
        (balance_column, "balance_column"),
    ]:
        if not isinstance(identifier, str) or not identifier_pattern.match(identifier):
            raise ValueError(f"Invalid identifier: {name}")
    
    # Validate amount: must be int (not bool) and > 0
    if isinstance(amount, bool) or not isinstance(amount, int):
        raise ValueError("amount must be an int")
    if amount <= 0:
        raise ValueError("amount must be positive")
    
    # Validate from_id and to_id differ
    if from_id == to_id:
        raise ValueError("from_id and to_id must differ")
    
    # Build SQL with double-quoted identifiers
    table_quoted = f'"{table}"'
    id_col_quoted = f'"{id_column}"'
    bal_col_quoted = f'"{balance_column}"'
    
    try:
        # Start transaction
        conn.execute("BEGIN")
        
        # Check both accounts exist and get their balances
        from_row = conn.execute(
            f"SELECT {bal_col_quoted} FROM {table_quoted} WHERE {id_col_quoted} = ?",
            (from_id,),
        ).fetchone()
        
        if from_row is None:
            raise ValueError("account not found")
        
        from_balance = from_row[0]
        
        to_row = conn.execute(
            f"SELECT {bal_col_quoted} FROM {table_quoted} WHERE {id_col_quoted} = ?",
            (to_id,),
        ).fetchone()
        
        if to_row is None:
            raise ValueError("account not found")
        
        to_balance = to_row[0]
        
        # Check sufficient funds
        if from_balance < amount:
            raise ValueError("insufficient funds")
        
        # Perform the transfer
        new_from_balance = from_balance - amount
        new_to_balance = to_balance + amount
        
        conn.execute(
            f"UPDATE {table_quoted} SET {bal_col_quoted} = ? WHERE {id_col_quoted} = ?",
            (new_from_balance, from_id),
        )
        
        conn.execute(
            f"UPDATE {table_quoted} SET {bal_col_quoted} = ? WHERE {id_col_quoted} = ?",
            (new_to_balance, to_id),
        )
        
        # Commit transaction
        conn.execute("COMMIT")
        
        return (new_from_balance, new_to_balance)
    
    except Exception as e:
        # Rollback on any error
        try:
            conn.execute("ROLLBACK")
        except Exception:
            pass
        raise
