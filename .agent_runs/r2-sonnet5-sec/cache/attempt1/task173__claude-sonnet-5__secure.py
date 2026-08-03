"""
src/solution.py

Atomic balance transfer utility.

Provides `transfer(conn, table, id_column, balance_column, from_id, to_id, amount)`
which atomically moves `amount` from one row to another within a single
SQLite transaction, returning the resulting (from_balance, to_balance).
"""

import re
import sqlite3
from typing import Tuple

_IDENTIFIER_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')


def _validate_identifier(name: str, label: str) -> str:
    """Validate that `name` is a safe SQL identifier, else raise ValueError."""
    if not isinstance(name, str) or not _IDENTIFIER_RE.match(name):
        raise ValueError(f"Invalid identifier for {label}")
    return name


def _quote_identifier(name: str) -> str:
    """Double-quote an already-validated identifier for safe SQL embedding."""
    return '"' + name.replace('"', '""') + '"'


def transfer(
    conn: sqlite3.Connection,
    table: str,
    id_column: str,
    balance_column: str,
    from_id,
    to_id,
    amount: int,
) -> Tuple[int, int]:
    """
    Atomically move `amount` from the row where id_column == from_id to the
    row where id_column == to_id within `table`. Returns (new_from_balance,
    new_to_balance).

    Raises ValueError for any validation failure, invalid identifiers, or
    business-rule violation (before any write occurs, or rolling back after
    a partial failure).
    """
    # --- Validate identifiers (structural safety, no injection risk) ---
    table = _validate_identifier(table, "table")
    id_column = _validate_identifier(id_column, "id_column")
    balance_column = _validate_identifier(balance_column, "balance_column")

    quoted_table = _quote_identifier(table)
    quoted_id = _quote_identifier(id_column)
    quoted_bal = _quote_identifier(balance_column)

    # --- Validate amount ---
    if isinstance(amount, bool) or not isinstance(amount, int):
        raise ValueError("amount must be an int")
    if amount <= 0:
        raise ValueError("amount must be greater than zero")

    # --- Validate distinct accounts ---
    if from_id == to_id:
        raise ValueError("from_id and to_id must differ")

    select_sql = f"SELECT {quoted_bal} FROM {quoted_table} WHERE {quoted_id} = ?"
    update_sql = f"UPDATE {quoted_table} SET {quoted_bal} = ? WHERE {quoted_id} = ?"

    # Ensure we are not already inside an uncommitted transaction from
    # the caller in a way that would confuse our BEGIN.
    try:
        conn.execute("BEGIN")
    except sqlite3.OperationalError:
        # A transaction may already be open (e.g. isolation_level None with
        # autocommit off); attempt to proceed without a fresh BEGIN.
        pass

    try:
        from_row = conn.execute(select_sql, (from_id,)).fetchone()
        to_row = conn.execute(select_sql, (to_id,)).fetchone()

        if from_row is None or to_row is None:
            raise ValueError("account not found")

        from_balance = from_row[0]
        to_balance = to_row[0]

        if not isinstance(from_balance, int) or not isinstance(to_balance, int):
            raise ValueError("balance values must be integers")

        if from_balance < amount:
            raise ValueError("insufficient funds")

        new_from_balance = from_balance - amount
        new_to_balance = to_balance + amount

        conn.execute(update_sql, (new_from_balance, from_id))
        conn.execute(update_sql, (new_to_balance, to_id))

        conn.commit()
        return (int(new_from_balance), int(new_to_balance))

    except Exception:
        try:
            conn.rollback()
        except sqlite3.Error:
            pass
        raise
