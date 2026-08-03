import re
import sqlite3
from typing import Any

_IDENTIFIER_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*", re.ASCII)


def _quote_identifier(identifier: str) -> str:
    if not isinstance(identifier, str) or _IDENTIFIER_RE.fullmatch(identifier) is None:
        raise ValueError("invalid identifier")
    return f'"{identifier}"'


def transfer(
    conn: sqlite3.Connection,
    table: str,
    id_column: str,
    balance_column: str,
    from_id: Any,
    to_id: Any,
    amount: int,
) -> tuple[int, int]:
    quoted_table = _quote_identifier(table)
    quoted_id = _quote_identifier(id_column)
    quoted_balance = _quote_identifier(balance_column)

    if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
        raise ValueError("amount must be a positive integer")
    if from_id == to_id:
        raise ValueError("source and destination accounts must differ")
    if not isinstance(conn, sqlite3.Connection):
        raise TypeError("conn must be a sqlite3.Connection")

    select_sql = (
        f"SELECT {quoted_balance} FROM {quoted_table} "
        f"WHERE {quoted_id} = ?"
    )
    debit_sql = (
        f"UPDATE {quoted_table} "
        f"SET {quoted_balance} = {quoted_balance} - ? "
        f"WHERE {quoted_id} = ?"
    )
    credit_sql = (
        f"UPDATE {quoted_table} "
        f"SET {quoted_balance} = {quoted_balance} + ? "
        f"WHERE {quoted_id} = ?"
    )

    transaction_active = conn.in_transaction

    try:
        if not transaction_active:
            conn.execute("BEGIN IMMEDIATE")
            transaction_active = True

        source_row = conn.execute(select_sql, (from_id,)).fetchone()
        destination_row = conn.execute(select_sql, (to_id,)).fetchone()

        if source_row is None or destination_row is None:
            raise ValueError("account not found")

        source_balance = source_row[0]
        destination_balance = destination_row[0]

        if (
            not isinstance(source_balance, int)
            or isinstance(source_balance, bool)
            or not isinstance(destination_balance, int)
            or isinstance(destination_balance, bool)
        ):
            raise ValueError("invalid balance")

        if source_balance < amount:
            raise ValueError("insufficient funds")

        debit_cursor = conn.execute(debit_sql, (amount, from_id))
        credit_cursor = conn.execute(credit_sql, (amount, to_id))

        if debit_cursor.rowcount != 1 or credit_cursor.rowcount != 1:
            raise ValueError("account not found")

        new_source_row = conn.execute(select_sql, (from_id,)).fetchone()
        new_destination_row = conn.execute(select_sql, (to_id,)).fetchone()

        if new_source_row is None or new_destination_row is None:
            raise ValueError("account not found")

        new_source_balance = new_source_row[0]
        new_destination_balance = new_destination_row[0]

        if (
            not isinstance(new_source_balance, int)
            or isinstance(new_source_balance, bool)
            or not isinstance(new_destination_balance, int)
            or isinstance(new_destination_balance, bool)
        ):
            raise ValueError("invalid balance")

        conn.commit()
        transaction_active = False
        return new_source_balance, new_destination_balance
    except BaseException:
        if transaction_active:
            try:
                conn.rollback()
            except sqlite3.Error:
                pass
        raise
