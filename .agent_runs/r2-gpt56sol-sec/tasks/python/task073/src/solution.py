"""Secure SQLite table creation utility."""

from __future__ import annotations

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
    """Create a SQLite table using validated identifiers and type strings.

    Raises:
        ValueError: If an identifier or type is invalid, no columns are
            supplied, column names collide case-insensitively, or the table
            already exists.
    """
    if not isinstance(table_name, str) or _IDENTIFIER_RE.fullmatch(table_name) is None:
        raise ValueError("invalid table name")

    if not isinstance(columns, Mapping):
        raise ValueError("columns must be a mapping")

    items: list[tuple[str, str]] = []
    seen_names: set[str] = set()

    for column_name, type_string in columns.items():
        if (
            not isinstance(column_name, str)
            or _IDENTIFIER_RE.fullmatch(column_name) is None
        ):
            raise ValueError("invalid column name")

        normalized_name = column_name.lower()
        if normalized_name in seen_names:
            raise ValueError("duplicate column name")
        seen_names.add(normalized_name)

        if (
            not isinstance(type_string, str)
            or not type_string.strip()
            or _TYPE_RE.fullmatch(type_string) is None
        ):
            raise ValueError("invalid column type")

        items.append((column_name, type_string))

    if not items:
        raise ValueError("columns must not be empty")

    definitions = ", ".join(
        f'"{column_name}" {type_string}' for column_name, type_string in items
    )
    statement = f'CREATE TABLE "{table_name}" ({definitions})'

    with sqlite3.connect(db_path) as connection:
        connection.execute("BEGIN IMMEDIATE")

        existing = connection.execute(
            """
            SELECT 1
            FROM sqlite_schema
            WHERE type = 'table'
              AND name = ? COLLATE NOCASE
            LIMIT 1
            """,
            (table_name,),
        ).fetchone()

        if existing is not None:
            raise ValueError("table already exists")

        connection.execute(statement)
