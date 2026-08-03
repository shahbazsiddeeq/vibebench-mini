import sqlite3
import re


def transfer(
    conn: sqlite3.Connection,
    table: str,
    id_column: str,
    balance_column: str,
    from_id,
    to_id,
    amount: int,
) -> tuple[int, int]:
    """
    Atomically transfer amount from one account to another.
    
    Args:
        conn: SQLite connection
        table: Table name (validated identifier)
        id_column: ID column name (validated identifier)
        balance_column: Balance column name (validated identifier)
        from_id: Source account ID
        to_id: Destination account ID
        amount: Amount to transfer (must be positive int)
    
    Returns:
        Tuple of (new_from_balance, new_to_balance)
    
    Raises:
        ValueError: If validation fails or insufficient funds
    """
    
    # Validate identifiers
    identifier_pattern = r"^[A-Za-z_][A-Za-z0-9_]*$"
    for identifier in [table, id_column, balance_column]:
        if not re.match(identifier_pattern, identifier):
            raise ValueError(f"Invalid identifier: {identifier}")
    
    # Validate amount
    if not isinstance(amount, int) or isinstance(amount, bool):
        raise ValueError("amount must be an int (not bool)")
    if amount <= 0:
        raise ValueError("amount must be > 0")
    
    # Validate from_id and to_id are different
    if from_id == to_id:
        raise ValueError("from_id and to_id must differ")
    
    # Start transaction
    try:
        # Check both accounts exist and get their balances
        from_row = conn.execute(
            f'SELECT "{balance_column}" FROM "{table}" WHERE "{id_column}" = ?',
            (from_id,),
        ).fetchone()
        
        if from_row is None:
            raise ValueError("account not found")
        
        from_balance = from_row[0]
        
        to_row = conn.execute(
            f'SELECT "{balance_column}" FROM "{table}" WHERE "{id_column}" = ?',
            (to_id,),
        ).fetchone()
        
        if to_row is None:
            raise ValueError("account not found")
        
        to_balance = to_row[0]
        
        # Check sufficient funds
        if from_balance < amount:
            raise ValueError("insufficient funds")
        
        # Perform the transfer within a transaction
        conn.execute("BEGIN")
        
        # Debit from source
        conn.execute(
            f'UPDATE "{table}" SET "{balance_column}" = "{balance_column}" - ? WHERE "{id_column}" = ?',
            (amount, from_id),
        )
        
        # Credit to destination
        conn.execute(
            f'UPDATE "{table}" SET "{balance_column}" = "{balance_column}" + ? WHERE "{id_column}" = ?',
            (amount, to_id),
        )
        
        conn.commit()
        
        # Return new balances
        new_from_balance = from_balance - amount
        new_to_balance = to_balance + amount
        
        return (new_from_balance, new_to_balance)
    
    except ValueError:
        # Rollback on any ValueError
        conn.rollback()
        raise
    except Exception:
        # Rollback on any other exception
        conn.rollback()
        raise
