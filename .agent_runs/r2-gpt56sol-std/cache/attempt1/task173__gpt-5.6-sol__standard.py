import re
import sqlite3
from typing import Any


_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


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

    if isinstance(amount, bool) or not isinstance(amount, int) or amount <= 0:
        raise ValueError("amount must be a positive integer")
    if from_id == to_id:
        raise ValueError("source and destination accounts must differ")

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

    started = False
    try:
        conn.execute("BEGIN IMMEDIATE")
        started = True

        from_row = conn.execute(select_sql, (from_id,)).fetchone()
        to_row = conn.execute(select_sql, (to_id,)).fetchone()

        if from_row is None or to_row is None:
            raise ValueError("account not found")

        if from_row[0] < amount:
            raise ValueError("insufficient funds")

        conn.execute(debit_sql, (amount, from_id))
        conn.execute(credit_sql, (amount, to_id))

        new_from_row = conn.execute(select_sql, (from_id,)).fetchone()
        new_to_row = conn.execute(select_sql, (to_id,)).fetchone()

        if new_from_row is None or new_to_row is None:
            raise ValueError("account not found")

        result = (new_from_row[0], new_to_row[0])
        conn.commit()
        return result
    except BaseException:
        if started:
            conn.rollback()
        raise
