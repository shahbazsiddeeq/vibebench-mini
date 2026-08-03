import re
import sqlite3

_IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _quote_identifier(name):
    """Validate an identifier against a strict whitelist and double-quote it."""
    if not isinstance(name, str) or not _IDENT_RE.match(name):
        raise ValueError(f"invalid SQL identifier: {name!r}")
    return '"' + name.replace('"', '""') + '"'


def bulk_update(conn, table, key_column, rows):
    """Apply a batch of per-row UPDATEs and return the total rows modified.

    For each dict in ``rows`` the non-key entries become the SET assignments
    and the ``key_column`` value becomes the WHERE lookup. All values are
    bound parameters; identifiers are whitelist-validated and double-quoted.
    The whole batch runs in one transaction and is rolled back on any error.
    The passed-in connection is not closed.
    """
    if not isinstance(rows, list):
        raise ValueError("rows must be a list")

    table_sql = _quote_identifier(table)
    key_sql = _quote_identifier(key_column)

    if not rows:
        return 0

    # Validate every row up front so a bad row cannot leave a partial batch.
    plans = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("each row must be a dict")
        if key_column not in row:
            raise ValueError(f"row is missing key column {key_column!r}")
        set_columns = [c for c in row if c != key_column]
        if not set_columns:
            raise ValueError("row has no columns to update")
        assignments = ", ".join(f"{_quote_identifier(c)} = ?" for c in set_columns)
        params = [row[c] for c in set_columns]
        params.append(row[key_column])
        sql = f"UPDATE {table_sql} SET {assignments} WHERE {key_sql} = ?"
        plans.append((sql, params))

    started = not conn.in_transaction
    total = 0
    try:
        if started:
            conn.execute("BEGIN")
        for sql, params in plans:
            cur = conn.execute(sql, params)
            total += cur.rowcount
        if started:
            conn.commit()
        return total
    except Exception:
        if started:
            conn.rollback()
        raise
