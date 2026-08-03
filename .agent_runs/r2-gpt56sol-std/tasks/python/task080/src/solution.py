"""Transactional SQLite batch insertion utilities."""

from __future__ import annotations

import re
import sqlite3
from collections.abc import Iterable, Mapping
from os import PathLike
from typing import Any


_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _quote_identifier(identifier: str) -> str:
    """Validate and quote an SQLite identifier."""
    if not isinstance(identifier, str) or not _IDENTIFIER.fullmatch(identifier):
        raise ValueError(f"Invalid SQL identifier: {identifier!r}")
    return f'"{identifier}"'


def batch_insert(
    db_path: str | bytes | PathLike[str] | PathLike[bytes],
    table: str,
    rows: Iterable[Mapping[str, Any]],
) -> int:
    """Insert all rows into an SQLite table in one transaction.

    Returns the number of inserted rows. Database and row-shape failures are
    raised as ``RuntimeError``. Unsafe table or column identifiers raise
    ``ValueError``.
    """
    quoted_table = _quote_identifier(table)

    try:
        row_list = list(rows)
    except Exception as exc:
        raise RuntimeError("Unable to read rows") from exc

    if not row_list:
        return 0

    first = row_list[0]
    if not isinstance(first, Mapping) or not first:
        raise RuntimeError("Each row must be a non-empty mapping")

    columns = list(first.keys())
    quoted_columns = [_quote_identifier(column) for column in columns]
    expected_keys = set(columns)

    values: list[tuple[Any, ...]] = []
    for row in row_list:
        if not isinstance(row, Mapping):
            raise RuntimeError("Each row must be a mapping")
        try:
            if len(row) != len(columns) or set(row.keys()) != expected_keys:
                raise RuntimeError("All rows must have identical keys")
            values.append(tuple(row[column] for column in columns))
        except RuntimeError:
            raise
        except Exception as exc:
            raise RuntimeError("Unable to read row values") from exc

    placeholders = ", ".join("?" for _ in columns)
    column_sql = ", ".join(quoted_columns)
    sql = f"INSERT INTO {quoted_table} ({column_sql}) VALUES ({placeholders})"

    conn: sqlite3.Connection | None = None
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("BEGIN")
        conn.executemany(sql, values)
        conn.commit()
    except Exception as exc:
        if conn is not None:
            try:
                conn.rollback()
            except sqlite3.Error:
                pass
        raise RuntimeError("Batch insert failed") from exc
    finally:
        if conn is not None:
            conn.close()

    return len(row_list)
