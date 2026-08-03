"""SQLite utilities for counting distinct column values."""

import re
import sqlite3
from contextlib import closing
from os import PathLike
from typing import Any, Dict, Union

_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\Z")


def _validate_identifier(identifier: str, name: str) -> None:
    if not isinstance(identifier, str) or _IDENTIFIER.fullmatch(identifier) is None:
        raise ValueError(f"Invalid {name} identifier: {identifier!r}")


def value_counts(
    db_path: Union[str, bytes, PathLike[str], PathLike[bytes]],
    table: str,
    column: str,
) -> Dict[Any, int]:
    """Return a mapping of distinct column values to their row counts."""
    _validate_identifier(table, "table")
    _validate_identifier(column, "column")

    query = (
        f'SELECT "{column}", COUNT(*) '
        f'FROM "{table}" '
        f'GROUP BY "{column}"'
    )

    with closing(sqlite3.connect(db_path)) as connection:
        rows = connection.execute(query).fetchall()

    return {value: count for value, count in rows}
