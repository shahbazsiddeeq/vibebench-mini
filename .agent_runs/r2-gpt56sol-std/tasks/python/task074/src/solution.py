import re
import sqlite3
from collections.abc import Mapping
from os import PathLike
from typing import Any


_IDENTIFIER_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")


def _validate_identifier(value: object) -> str:
    if not isinstance(value, str) or _IDENTIFIER_RE.fullmatch(value) is None:
        raise ValueError(f"Invalid SQL identifier: {value!r}")
    return value


def _quote_identifier(identifier: str) -> str:
    return f'"{identifier}"'


def upsert(
    db_path: str | PathLike[str],
    table: str,
    record: Mapping[str, Any],
    key: str,
) -> None:
    """Insert a record or update its supplied non-key columns on key conflict."""
    table = _validate_identifier(table)
    key = _validate_identifier(key)

    columns = list(record.keys())
    for column in columns:
        _validate_identifier(column)

    if key not in record:
        raise KeyError(key)

    quoted_columns = ", ".join(_quote_identifier(column) for column in columns)
    placeholders = ", ".join("?" for _ in columns)
    quoted_key = _quote_identifier(key)

    update_columns = [column for column in columns if column != key]
    if update_columns:
        assignments = ", ".join(
            f"{_quote_identifier(column)} = excluded.{_quote_identifier(column)}"
            for column in update_columns
        )
        conflict_action = f"DO UPDATE SET {assignments}"
    else:
        conflict_action = "DO NOTHING"

    sql = (
        f"INSERT INTO {_quote_identifier(table)} ({quoted_columns}) "
        f"VALUES ({placeholders}) "
        f"ON CONFLICT ({quoted_key}) {conflict_action}"
    )
    values = [record[column] for column in columns]

    connection = sqlite3.connect(db_path)
    try:
        with connection:
            connection.execute(sql, values)
    finally:
        connection.close()
