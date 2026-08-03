"""SQLite Table Creator.

Provides create_table(db_path, table_name, columns) which safely builds a
CREATE TABLE statement from validated identifiers and type strings.
"""

import re
import sqlite3

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_TYPE_RE = re.compile(r"^[A-Za-z0-9_ ()]*$")


def _validate_identifier(name):
    if not isinstance(name, str) or not _IDENTIFIER_RE.match(name):
        raise ValueError("Invalid identifier")
    return name


def _validate_type(type_str):
    if not isinstance(type_str, str) or not _TYPE_RE.match(type_str):
        raise ValueError("Invalid type string")
    return type_str


def _quote_identifier(name):
    return '"' + name.replace('"', '""') + '"'


def create_table(db_path, table_name, columns):
    if not isinstance(columns, dict) or not columns:
        raise ValueError("columns must be a non-empty dict")

    _validate_identifier(table_name)

    column_defs = []
    for col_name, col_type in columns.items():
        _validate_identifier(col_name)
        _validate_type(col_type)
        column_defs.append(f"{_quote_identifier(col_name)} {col_type}")

    quoted_table = _quote_identifier(table_name)
    columns_sql = ", ".join(column_defs)
    create_sql = f"CREATE TABLE {quoted_table} ({columns_sql})"

    try:
        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' "
                "AND name = ? COLLATE NOCASE",
                (table_name,),
            )
            if cursor.fetchone() is not None:
                raise ValueError("Table already exists")

            cursor.execute(create_sql)
            conn.commit()
        finally:
            conn.close()
    except sqlite3.Error as exc:
        raise ValueError("Database error while creating table") from exc
