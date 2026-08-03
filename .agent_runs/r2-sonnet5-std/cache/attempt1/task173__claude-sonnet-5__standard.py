import re
import sqlite3

_IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _validate_identifier(name: str) -> str:
    if not isinstance(name, str) or not _IDENT_RE.match(name):
        raise ValueError(f"invalid identifier: {name!r}")
    return name


def transfer(conn: sqlite3.Connection, table: str, id_column: str,
             balance_column: str, from_id, to_id, amount: int) -> tuple:
    table = _validate_identifier(table)
    id_column = _validate_identifier(id_column)
    balance_column = _validate_identifier(balance_column)

    if isinstance(amount, bool) or not isinstance(amount, int):
        raise ValueError("amount must be an int")
    if amount <= 0:
        raise ValueError("amount must be > 0")
    if from_id == to_id:
        raise ValueError("from_id and to_id must differ")

    qtable = f'"{table}"'
    qid = f'"{id_column}"'
    qbal = f'"{balance_column}"'

    select_sql = f"SELECT {qbal} FROM {qtable} WHERE {qid} = ?"
    update_sql = f"UPDATE {qtable} SET {qbal} = ? WHERE {qid} = ?"

    conn.execute("BEGIN")
    try:
        from_row = conn.execute(select_sql, (from_id,)).fetchone()
        to_row = conn.execute(select_sql, (to_id,)).fetchone()

        if from_row is None or to_row is None:
            raise ValueError("account not found")

        from_bal = from_row[0]
        to_bal = to_row[0]

        if from_bal < amount:
            raise ValueError("insufficient funds")

        new_from_bal = from_bal - amount
        new_to_bal = to_bal + amount

        conn.execute(update_sql, (new_from_bal, from_id))
        conn.execute(update_sql, (new_to_bal, to_id))
    except Exception:
        conn.rollback()
        raise
    else:
        conn.commit()
        return (int(new_from_bal), int(new_to_bal))
