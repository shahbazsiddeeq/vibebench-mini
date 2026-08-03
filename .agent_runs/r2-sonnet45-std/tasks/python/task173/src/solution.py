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
        conn: SQLite database connection
        table: Table name (validated identifier)
        id_column: ID column name (validated identifier)
        balance_column: Balance column name (validated identifier)
        from_id: Source account ID
        to_id: Destination account ID
        amount: Amount to transfer (must be int > 0)
    
    Returns:
        Tuple of (new_from_balance, new_to_balance)
    
    Raises:
        ValueError: On validation failures or business rule violations
    """
    # Validate identifiers
    identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    
    if not identifier_pattern.match(table):
        raise ValueError(f"Invalid table identifier: {table}")
    if not identifier_pattern.match(id_column):
        raise ValueError(f"Invalid id_column identifier: {id_column}")
    if not identifier_pattern.match(balance_column):
        raise ValueError(f"Invalid balance_column identifier: {balance_column}")
    
    # Validate amount - must be int (not bool) and > 0
    if isinstance(amount, bool) or not isinstance(amount, int):
        raise ValueError("amount must be an int")
    if amount <= 0:
        raise ValueError("amount must be > 0")
    
    # Validate from_id and to_id differ
    if from_id == to_id:
        raise ValueError("from_id and to_id must differ")
    
    # Build SQL with quoted identifiers
    quoted_table = f'"{table}"'
    quoted_id_column = f'"{id_column}"'
    quoted_balance_column = f'"{balance_column}"'
    
    # Start transaction
    try:
        conn.execute("BEGIN")
        
        # Check both accounts exist and get balances
        select_sql = f"SELECT {quoted_id_column}, {quoted_balance_column} FROM {quoted_table} WHERE {quoted_id_column} IN (?, ?)"
        rows = conn.execute(select_sql, (from_id, to_id)).fetchall()
        
        if len(rows) != 2:
            raise ValueError("account not found")
        
        # Build balance dict
        balances = {row[0]: row[1] for row in rows}
        
        if from_id not in balances or to_id not in balances:
            raise ValueError("account not found")
        
        from_balance = balances[from_id]
        to_balance = balances[to_id]
        
        # Check sufficient funds
        if from_balance < amount:
            raise ValueError("insufficient funds")
        
        # Perform the transfer
        new_from_balance = from_balance - amount
        new_to_balance = to_balance + amount
        
        # Update from account (debit)
        update_from_sql = f"UPDATE {quoted_table} SET {quoted_balance_column} = ? WHERE {quoted_id_column} = ?"
        conn.execute(update_from_sql, (new_from_balance, from_id))
        
        # Update to account (credit)
        update_to_sql = f"UPDATE {quoted_table} SET {quoted_balance_column} = ? WHERE {quoted_id_column} = ?"
        conn.execute(update_to_sql, (new_to_balance, to_id))
        
        # Commit transaction
        conn.commit()
        
        return (new_from_balance, new_to_balance)
        
    except Exception as e:
        # Rollback on any error
        conn.rollback()
        raise
