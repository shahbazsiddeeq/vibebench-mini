import csv
import re
import sqlite3
from os import PathLike
from typing import Union

__all__ = ["csv_to_sqlite"]

_IDENTIFIER_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")


def _validate_identifier(name: object, description: str) -> str:
    if not isinstance(name, str) or _IDENTIFIER_RE.fullmatch(name) is None:
        raise ValueError(f"invalid {description}: {name!r}")
    return name


def csv_to_sqlite(
    csv_path: Union[str, PathLike[str]],
    db_path: Union[str, PathLike[str]],
    table_name: str,
) -> int:
    """Import a header-based CSV file into a newly created SQLite table."""
    # Opening the CSV first preserves FileNotFoundError for a missing input file.
    with open(csv_path, "r", newline="") as csv_file:
        table_name = _validate_identifier(table_name, "table name")
        reader = csv.reader(csv_file)

        try:
            header = next(reader)
        except StopIteration as exc:
            raise ValueError("CSV file has no header") from exc

        for column in header:
            _validate_identifier(column, "column name")

        # SQLite column names are case-insensitive.
        if len({column.lower() for column in header}) != len(header):
            raise ValueError("CSV header contains duplicate column names")

        quoted_table = f'"{table_name}"'
        quoted_columns = [f'"{column}"' for column in header]

        with sqlite3.connect(db_path) as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                existing = connection.execute(
                    """
                    SELECT 1
                    FROM sqlite_master
                    WHERE name = ? COLLATE NOCASE
                    LIMIT 1
                    """,
                    (table_name,),
                ).fetchone()
                if existing is not None:
                    raise ValueError(f"table {table_name!r} already exists")

                # SQLite cannot create a table with zero columns.
                if not header:
                    connection.commit()
                    return 0

                definitions = ", ".join(
                    f"{column} TEXT" for column in quoted_columns
                )
                connection.execute(
                    f"CREATE TABLE {quoted_table} ({definitions})"
                )

                placeholders = ", ".join("?" for _ in header)
                insert_sql = (
                    f"INSERT INTO {quoted_table} "
                    f"({', '.join(quoted_columns)}) VALUES ({placeholders})"
                )

                inserted = 0
                for row in reader:
                    if len(row) != len(header):
                        raise ValueError(
                            "CSV row has a different number of fields than the header"
                        )
                    connection.execute(insert_sql, row)
                    inserted += 1

                connection.commit()
                return inserted
            except Exception:
                connection.rollback()
                raise
