import sqlite3
import re

def transfer(conn: sqlite3.Connection, table: str, id_column: str, balance_column: str, from_id, to_id, amount: int) -> tuple[int, int]:
    # Validate identifiers
    identifier_pattern = r'^[A-Za-z_][A-Za-z0-9_]*$'
    if not re.match(identifier_pattern, table):
        raise ValueError("Invalid table name")
    if not re.match(identifier_pattern, id_column):
        raise ValueError("Invalid id_column name")
    if not re.match(identifier_pattern, balance_column):
        raise ValueError("Invalid balance_column name")
    
    # Validate amount
    if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
        raise ValueError("Amount must be a positive integer")
    
    # Validate from_id and to_id
    if from_id == to_id:
        raise ValueError("from_id and to_id must differ")
    
    # Prepare SQL with safe identifiers
    table = f'"{table}"'
    id_column = f'"{id_column}"'
    balance_column = f'"{balance_column}"'
    
    try:
        with conn:
            # Check if both accounts exist
            cursor = conn.execute(
                f"SELECT {balance_column} FROM {table} WHERE {id_column} = ? OR {id_column} = ?",
                (from_id, to_id)
            )
            rows = cursor.fetchall()
            if len(rows) != 2:
                raise ValueError("account not found")
            
            # Extract balances
            from_balance, to_balance = None, None
            for row in rows:
                if row[0] == from_id:
                    from_balance = row[1]
                else:
                    to_balance = row[1]
            
            # Check if from_balance is sufficient
            if from_balance < amount:
                raise ValueError("insufficient funds")
            
            # Perform the transfer
            new_from_balance = from_balance - amount
            new_to_balance = to_balance + amount
            
            # Update balances atomically
            conn.execute(
                f"UPDATE {table} SET {balance_column} = ? WHERE {id_column} = ?",
                (new_from_balance, from_id)
            )
            conn.execute(
                f"UPDATE {table} SET {balance_column} = ? WHERE {id_column} = ?",
                (new_to_balance, to_id)
            )
            
            return new_from_balance, new_to_balance
    
    except sqlite3.Error as e:
        raise ValueError("Database error") from e
