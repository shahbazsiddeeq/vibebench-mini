import re
import sqlite3

_IDENT_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
_TYPE_RE = re.compile(r'^[A-Za-z0-9_ ()]*$')


def create_table(db_path, table_name, columns):
    if not isinstance(table_name, str) or not _IDENT_RE.match(table_name):
        raise ValueError(f"Invalid table name: {table_name!r}")

    if not columns:
        raise ValueError("columns must not be empty")

    for col_name, col_type in columns.items():
        if not isinstance(col_name, str) or not _IDENT_RE.match(col_name):
            raise ValueError(f"Invalid column name: {col_name!r}")
        if not isinstance(col_type, str) or not _TYPE_RE.match(col_type):
            raise ValueError(f"Invalid column type: {col_type!r}")

    with sqlite3.connect(db_path) as conn:
        cur = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' COLLATE NOCASE AND name = ? COLLATE NOCASE",
            (table_name,)
        )
        if cur.fetchone() is not None:
            raise ValueError(f"Table already exists: {table_name!r}")

        col_defs = ", ".join(
            f'"{col_name}" {col_type}' for col_name, col_type in columns.items()
        )
        sql = f'CREATE TABLE "{table_name}" ({col_defs})'
        conn.execute(sql)
        conn.commit()
