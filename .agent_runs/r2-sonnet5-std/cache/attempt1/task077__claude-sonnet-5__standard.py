import csv
import os
import re
import sqlite3

_IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _validate_identifier(name):
    if not _IDENT_RE.match(name):
        raise ValueError(f"Invalid identifier: {name!r}")
    return name


def csv_to_sqlite(csv_path, db_path, table_name):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"No such file: {csv_path!r}")

    _validate_identifier(table_name)

    with open(csv_path, newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            header = []

        for col in header:
            _validate_identifier(col)

        rows = list(reader)

    quoted_table = f'"{table_name}"'
    quoted_cols = [f'"{col}"' for col in header]

    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()

        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        if cur.fetchone() is not None:
            raise ValueError(f"Table already exists: {table_name!r}")

        if quoted_cols:
            cols_def = ", ".join(f"{c} TEXT" for c in quoted_cols)
        else:
            cols_def = ""

        create_sql = f"CREATE TABLE {quoted_table} ({cols_def})"
        cur.execute(create_sql)

        count = 0
        if quoted_cols:
            placeholders = ", ".join("?" for _ in quoted_cols)
            insert_sql = (
                f"INSERT INTO {quoted_table} ({', '.join(quoted_cols)}) "
                f"VALUES ({placeholders})"
            )
            for row in rows:
                cur.execute(insert_sql, row)
                count += 1

        conn.commit()
        return count
    finally:
        conn.close()
