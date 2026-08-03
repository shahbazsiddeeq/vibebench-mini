import re
import sqlite3
from collections.abc import Mapping
from os import PathLike
from typing import Any


_IDENTIFIER_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")
_TYPE_RE = re.compile(r"[A-Za-z0-9_ ()]+\Z")


def create_table(
    db_path: str | bytes | PathLike[str] | PathLike[bytes],
    table_name: str,
    columns: Mapping[str, str],
) -> None:
    """Create a SQLite table after validating all interpolated SQL parts."""
    if not isinstance(table_name, str) or _IDENTIFIER_RE.fullmatch(table_name) is None:
        raise ValueError(f"Invalid table name: {table_name!r}")

    if not isinstance(columns, Mapping) or not columns:
        raise ValueError("columns must be a non-empty mapping")

    definitions: list[str] = []
    seen_names: set[str] = set()

    for column_name, type_string in columns.items():
        if (
            not isinstance(column_name, str)
            or _IDENTIFIER_RE.fullmatch(column_name) is None
        ):
            raise ValueError(f"Invalid column name: {column_name!r}")

        normalized_name = column_name.lower()
        if normalized_name in seen_names:
            raise ValueError(f"Duplicate column name: {column_name!r}")
        seen_names.add(normalized_name)

        if (
            not isinstance(type_string, str)
            or _TYPE_RE.fullmatch(type_string) is None
        ):
            raise ValueError(f"Invalid type string for column {column_name!r}")

        definitions.append(f'"{column_name}" {type_string}')

    statement = f'CREATE TABLE "{table_name}" ({", ".join(definitions)})'

    with sqlite3.connect(db_path) as connection:
        connection.execute("BEGIN IMMEDIATE")

        existing = connection.execute(
            """
            SELECT 1
            FROM sqlite_master
            WHERE type = 'table' AND name = ? COLLATE NOCASE
            LIMIT 1
            """,
            (table_name,),
        ).fetchone()

        if existing is not None:
            raise ValueError(f"Table already exists: {table_name!r}")

        connection.execute(statement)
