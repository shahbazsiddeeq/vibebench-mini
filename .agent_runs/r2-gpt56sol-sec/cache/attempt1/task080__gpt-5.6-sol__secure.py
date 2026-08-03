"""Secure SQLite batch insertion utility."""

from __future__ import annotations

import os
import re
import sqlite3
from collections.abc import Iterable, Mapping
from typing import Any


_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\Z")


def _validate_identifier(identifier: object, kind: str) -> str:
    if not isinstance(identifier, str) or not _IDENTIFIER.fullmatch(identifier):
        raise ValueError(f"invalid {kind} identifier")
    return identifier


def _validate_db_path(db_path: object) -> str | bytes:
    try:
        path = os.fspath(db_path)
    except TypeError:
        raise ValueError("invalid database path") from None

    if not isinstance(path, (str, bytes)) or not path:
        raise ValueError("invalid database path")

    nul = "\0" if isinstance(path, str) else b"\0"
    if nul in path:
        raise ValueError("invalid database path")

    return path


def _prepare_rows(
    rows: Iterable[Mapping[str, Any]],
) -> tuple[tuple[str, ...], list[tuple[Any, ...]]]:
    if isinstance(rows, (str, bytes, bytearray, Mapping)):
        raise RuntimeError("batch insert failed")

    try:
        iterator = iter(rows)
    except TypeError:
        raise RuntimeError("batch insert failed") from None

    columns: tuple[str, ...] | None = None
    expected_keys: frozenset[str] | None = None
    values: list[tuple[Any, ...]] = []

    try:
        for row in iterator:
            if not isinstance(row, Mapping):
                raise RuntimeError("batch insert failed")

            keys = tuple(row.keys())
            for key in keys:
                _validate_identifier(key, "column")

            if columns is None:
                if not keys or len(set(keys)) != len(keys):
                    raise RuntimeError("batch insert failed")
                columns = keys
                expected_keys = frozenset(keys)
            elif len(keys) != len(columns) or frozenset(keys) != expected_keys:
                raise RuntimeError("batch insert failed")

            values.append(tuple(row[column] for column in columns))
    except (RuntimeError, ValueError):
        raise
    except Exception:
        raise RuntimeError("batch insert failed") from None

    return columns or (), values


def batch_insert(
    db_path: str | bytes | os.PathLike[str] | os.PathLike[bytes],
    table: str,
    rows: Iterable[Mapping[str, Any]],
) -> int:
    """Insert all rows atomically and return the number of submitted rows.

    Table and column names must be simple SQLite identifiers. All rows must
    contain exactly the same keys. Database or insertion failures are exposed
    as a generic ``RuntimeError`` and the transaction is rolled back.
    """
    path = _validate_db_path(db_path)
    table_name = _validate_identifier(table, "table")
    columns, values = _prepare_rows(rows)

    if not values:
        return 0

    quoted_table = f'"{table_name}"'
    quoted_columns = ", ".join(f'"{column}"' for column in columns)
    placeholders = ", ".join("?" for _ in columns)
    statement = (
        f"INSERT INTO {quoted_table} ({quoted_columns}) "
        f"VALUES ({placeholders})"
    )

    connection: sqlite3.Connection | None = None
    try:
        connection = sqlite3.connect(path, isolation_level=None, uri=False)
        connection.execute("BEGIN")
        connection.executemany(statement, values)
        connection.execute("COMMIT")
    except Exception:
        if connection is not None:
            try:
                connection.execute("ROLLBACK")
            except Exception:
                pass
        raise RuntimeError("batch insert failed") from None
    finally:
        if connection is not None:
            try:
                connection.close()
            except Exception:
                pass

    return len(values)
