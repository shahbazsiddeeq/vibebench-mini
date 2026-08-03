import re
import sqlite3

_IDENT_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')


def _validate_identifier(name):
    if not isinstance(name, str) or not _IDENT_RE.match(name):
        raise ValueError(f"Invalid identifier: {name!r}")
    return name


def upsert(db_path, table, record, key):
    if key not in record:
        raise KeyError(key)

    _validate_identifier(table)
    _validate_identifier(key)
    for col in record:
        _validate_identifier(col)

    columns = list(record.keys())
    quoted_table = f'"{table}"'
    quoted_key = f'"{key}"'
    quoted_columns = [f'"{c}"' for c in columns]

    col_list = ", ".join(quoted_columns)
    placeholders = ", ".join(["?"] * len(columns))
    values = [record[c] for c in columns]

    update_cols = [c for c in columns if c != key]

    if update_cols:
        set_clause = ", ".join(f'"{c}" = excluded."{c}"' for c in update_cols)
        sql = (
            f'INSERT INTO {quoted_table} ({col_list}) VALUES ({placeholders}) '
            f'ON CONFLICT({quoted_key}) DO UPDATE SET {set_clause}'
        )
    else:
        sql = (
            f'INSERT INTO {quoted_table} ({col_list}) VALUES ({placeholders}) '
            f'ON CONFLICT({quoted_key}) DO NOTHING'
        )

    with sqlite3.connect(db_path) as conn:
        conn.execute(sql, values)
        conn.commit()
