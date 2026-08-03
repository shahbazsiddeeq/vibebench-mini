"""Secure CSV-to-SQLite importer."""

from __future__ import annotations

import csv
import os
import re
import sqlite3
from typing import Union


_IDENTIFIER_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")
PathType = Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]


def _validate_identifier(name: str, kind: str) -> None:
    if not isinstance(name, str) or _IDENTIFIER_RE.fullmatch(name) is None:
        raise ValueError(f"Invalid {kind} identifier")


def _quote_identifier(name: str) -> str:
    # The caller validates identifiers before quoting.
    return f'"{name}"'


def csv_to_sqlite(
    csv_path: PathType,
    db_path: PathType,
    table_name: str,
) -> int:
    """Import a header-based CSV into a newly created SQLite table.

    Every column is created with SQLite type TEXT. The operation is
    transactional, so malformed rows do not leave a partially imported table.
    """
    # Opening first guarantees a missing CSV raises FileNotFoundError.
    with open(csv_path, "r", encoding="utf-8", newline="") as csv_file:
        reader = csv.reader(csv_file)

        try:
            header = next(reader)
        except StopIteration as exc:
            raise ValueError("CSV file has no header") from exc

        _validate_identifier(table_name, "table")

        for column in header:
            _validate_identifier(column, "column")

        # SQLite identifiers are case-insensitive, so these would collide.
        normalized_columns = [column.lower() for column in header]
        if len(normalized_columns) != len(set(normalized_columns)):
            raise ValueError("CSV header contains duplicate column names")

        if not header:
            # A blank header line represents the specified zero-column case.
            if next(reader, None) is not None:
                raise ValueError("CSV data cannot exist without columns")

        quoted_table = _quote_identifier(table_name)

        connection = sqlite3.connect(db_path)
        try:
            connection.execute("BEGIN IMMEDIATE")

            existing = connection.execute(
                """
                SELECT 1
                FROM sqlite_schema
                WHERE name = ? COLLATE NOCASE
                  AND type IN ('table', 'view')
                LIMIT 1
                """,
                (table_name,),
            ).fetchone()
            if existing is not None:
                raise ValueError("A table with that name already exists")

            if not header:
                connection.commit()
                return 0

            column_definitions = ", ".join(
                f"{_quote_identifier(column)} TEXT" for column in header
            )
            connection.execute(
                f"CREATE TABLE {quoted_table} ({column_definitions})"
            )

            placeholders = ", ".join("?" for _ in header)
            insert_sql = f"INSERT INTO {quoted_table} VALUES ({placeholders})"

            inserted = 0
            cursor = connection.cursor()
            for row in reader:
                if len(row) != len(header):
                    raise ValueError(
                        "CSV row has a different number of fields than the header"
                    )
                cursor.execute(insert_sql, row)
                inserted += 1

            connection.commit()
            return inserted
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
