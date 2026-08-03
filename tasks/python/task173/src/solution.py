import re
import sqlite3

_IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _quote_identifier(name):
    """Validate an identifier against a strict whitelist and double-quote it."""
    if not isinstance(name, str) or not _IDENT_RE.match(name):
        raise ValueError(f"invalid SQL identifier: {name!r}")
    return '"' + name.replace('"', '""') + '"'


def transfer(conn, table, id_column, balance_column, from_id, to_id, amount):
    """Atomically move ``amount`` from ``from_id`` to ``to_id``.

    Returns ``(new_from_balance, new_to_balance)``. Identifiers are
    whitelist-validated and double-quoted; all values are bound parameters.
    The debit and credit happen in a single transaction: on any failure the
    transaction is rolled back so both balances are left unchanged. The
    passed-in connection is not closed.
    """
    table_sql = _quote_identifier(table)
    id_sql = _quote_identifier(id_column)
    bal_sql = _quote_identifier(balance_column)

    # amount must be a real int (bool is a subclass of int -> reject) and > 0.
    if isinstance(amount, bool) or not isinstance(amount, int):
        raise ValueError("amount must be an int")
    if amount <= 0:
        raise ValueError("amount must be greater than 0")
    if from_id == to_id:
        raise ValueError("from_id and to_id must differ")

    started = not conn.in_transaction
    try:
        if started:
            conn.execute("BEGIN")

        cur = conn.execute(
            f"SELECT {bal_sql} FROM {table_sql} WHERE {id_sql} = ?", (from_id,)
        )
        src = cur.fetchone()
        cur = conn.execute(
            f"SELECT {bal_sql} FROM {table_sql} WHERE {id_sql} = ?", (to_id,)
        )
        dst = cur.fetchone()

        if src is None or dst is None:
            raise ValueError("account not found")

        src_balance = src[0]
        dst_balance = dst[0]

        if src_balance < amount:
            raise ValueError("insufficient funds")

        conn.execute(
            f"UPDATE {table_sql} SET {bal_sql} = {bal_sql} - ? WHERE {id_sql} = ?",
            (amount, from_id),
        )
        conn.execute(
            f"UPDATE {table_sql} SET {bal_sql} = {bal_sql} + ? WHERE {id_sql} = ?",
            (amount, to_id),
        )

        new_from = src_balance - amount
        new_to = dst_balance + amount

        if started:
            conn.commit()
        return (new_from, new_to)
    except Exception:
        if started:
            conn.rollback()
        raise
