import sqlite3
import re


def transfer(
    conn: sqlite3.Connection,
    table: str,
    id_column: str,
    balance_column: str,
    from_id,
    to_id,
    amount: int
) -> tuple[int, int]:
    """
    Atomically transfer amount from one account to another within a transaction.
    
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
    # Validate identifiers against ^[A-Za-z_][A-Za-z0-9_]*$
    identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    
    if not identifier_pattern.match(table):
        raise ValueError("Invalid table identifier")
    if not identifier_pattern.match(id_column):
        raise ValueError("Invalid id_column identifier")
    if not identifier_pattern.match(balance_column):
        raise ValueError("Invalid balance_column identifier")
    
    # Validate amount: must be int (not bool) and > 0
    if isinstance(amount, bool):
        raise ValueError("Amount cannot be a boolean")
    if not isinstance(amount, int):
        raise ValueError("Amount must be an integer")
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")
    
    # Validate from_id and to_id differ
    if from_id == to_id:
        raise ValueError("Source and destination accounts must differ")
    
    # Double-quote identifiers for SQL
    quoted_table = f'"{table}"'
    quoted_id_column = f'"{id_column}"'
    quoted_balance_column = f'"{balance_column}"'
    
    try:
        # Begin transaction using context manager
        with conn:
            # Check both accounts exist and get their balances
            check_query = f"""
                SELECT {quoted_id_column}, {quoted_balance_column}
                FROM {quoted_table}
                WHERE {quoted_id_column} IN (?, ?)
            """
            rows = conn.execute(check_query, (from_id, to_id)).fetchall()
            
            if len(rows) != 2:
                raise ValueError("account not found")
            
            # Extract balances
            balances_dict = {row[0]: row[1] for row in rows}
            
            if from_id not in balances_dict or to_id not in balances_dict:
                raise ValueError("account not found")
            
            from_balance = balances_dict[from_id]
            to_balance = balances_dict[to_id]
            
            # Check sufficient funds
            if from_balance < amount:
                raise ValueError("insufficient funds")
            
            # Perform the transfer
            # Debit from source
            debit_query = f"""
                UPDATE {quoted_table}
                SET {quoted_balance_column} = {quoted_balance_column} - ?
                WHERE {quoted_id_column} = ?
            """
            conn.execute(debit_query, (amount, from_id))
            
            # Credit to destination
            credit_query = f"""
                UPDATE {quoted_table}
                SET {quoted_balance_column} = {quoted_balance_column} + ?
                WHERE {quoted_id_column} = ?
            """
            conn.execute(credit_query, (amount, to_id))
            
            # Calculate new balances
            new_from_balance = from_balance - amount
            new_to_balance = to_balance + amount
            
            # Transaction will be committed automatically when exiting the context manager
            return (new_from_balance, new_to_balance)
            
    except ValueError:
        # Re-raise ValueError as-is (transaction already rolled back by context manager)
        raise
    except Exception as e:
        # Any other exception should also roll back (handled by context manager)
        raise
