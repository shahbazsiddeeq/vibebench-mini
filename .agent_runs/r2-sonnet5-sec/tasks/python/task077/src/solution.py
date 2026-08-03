"""
CSV to SQLite Importer
=======================

A small, security-conscious utility that imports a CSV file into a new
SQLite table.

Design notes / security considerations
---------------------------------------
* All identifiers (table name and column/header names) are validated
  against a strict allow-list pattern (``[A-Za-z_][A-Za-z0-9_]*``) before
  being used in any SQL statement. This prevents SQL injection via
  malicious table/column names, since untrusted strings are never
  concatenated into SQL without validation.
* All *data values* are passed to SQLite using parameterized queries
  (``?`` placeholders) -- never string-interpolated -- eliminating SQL
  injection through row data as well.
* The CSV file is opened with `newline=""` as recommended by the
  ``csv`` module documentation to ensure correct handling of embedded
  newlines/quoting.
* No use of ``eval``/``exec``/``os.system`` or other dangerous
  constructs; only the standard library (`csv`, `sqlite3`, `os`,
  `re`) is used.
* Errors that are part of the documented contract (``FileNotFoundError``
  for a missing CSV, ``ValueError`` for invalid identifiers or an
  already-existing table) are raised with clear, non-sensitive
  messages. Any other unexpected failure while touching the database is
  wrapped into a generic ``RuntimeError`` so internal details (e.g.
  file-system paths, stack traces, driver internals) are not leaked to
  callers.
"""

from __future__ import annotations

import csv
import os
import re
import sqlite3
from typing import Final

_IDENTIFIER_RE: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _validate_identifier(name: str, kind: str = "identifier") -> str:
    """Validate that *name* is a safe SQL identifier.

    Raises ValueError if it does not match the required pattern.
    Returns the name unchanged on success.
    """
    if not isinstance(name, str) or not _IDENTIFIER_RE.match(name):
        raise ValueError(f"Invalid {kind}: {name!r}")
    return name


def _quote_identifier(name: str) -> str:
    """Double-quote an already-validated identifier for safe SQL use."""
    # Identifiers matching _IDENTIFIER_RE never contain a double quote,
    # so simple wrapping is sufficient and safe.
    return f'"{name}"'


def csv_to_sqlite(csv_path: str, db_path: str, table_name: str) -> int:
    """Import a CSV file into a new SQLite table.

    :param csv_path: Path to the source CSV file. First line must be the
        header row.
    :param db_path: Path to the SQLite database file (created if
        necessary).
    :param table_name: Name of the table to create. Must match
        ``[A-Za-z_][A-Za-z0-9_]*``.
    :returns: Number of data rows inserted.
    :raises FileNotFoundError: if ``csv_path`` does not exist.
    :raises ValueError: if ``table_name`` or any header name is not a
        valid identifier, or if a table with that name already exists.
    """
    if not isinstance(csv_path, str) or not isinstance(db_path, str):
        raise ValueError("csv_path and db_path must be strings")

    # Validate table name up front (before touching the filesystem for
    # the CSV, matching the documented contract precisely, but we also
    # need to check file existence -- order doesn't materially matter
    # for security, so validate identifiers first since they are cheap
    # and purely syntactic).
    _validate_identifier(table_name, kind="table name")

    if not os.path.isfile(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path!r}")

    # Read header + rows from the CSV.
    try:
        with open(csv_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            try:
                header = next(reader)
            except StopIteration:
                header = []
            rows = list(reader)
    except (OSError, UnicodeDecodeError) as exc:
        raise RuntimeError("Failed to read CSV file") from exc

    # Validate each header/column name.
    validated_columns = [_validate_identifier(col, kind="column name") for col in header]

    quoted_table = _quote_identifier(table_name)
    quoted_columns = [_quote_identifier(col) for col in validated_columns]

    conn: sqlite3.Connection | None = None
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # Check whether the table already exists.
        cur.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
            (table_name,),
        )
        if cur.fetchone() is not None:
            raise ValueError(f"Table already exists: {table_name!r}")

        if quoted_columns:
            columns_sql = ", ".join(f"{col} TEXT" for col in quoted_columns)
            create_sql = f"CREATE TABLE {quoted_table} ({columns_sql})"
        else:
            # No columns at all (e.g. empty header line). Create an
            # empty table with no columns.
            create_sql = f"CREATE TABLE {quoted_table} ()"

        cur.execute(create_sql)

        inserted = 0
        if quoted_columns:
            placeholders = ", ".join("?" for _ in quoted_columns)
            insert_sql = (
                f"INSERT INTO {quoted_table} "
                f"({', '.join(quoted_columns)}) VALUES ({placeholders})"
            )
            n_cols = len(validated_columns)
            for row in rows:
                # Normalize row length to match header length, guarding
                # against malformed/short/long CSV rows without raising.
                if len(row) < n_cols:
                    row = row + [""] * (n_cols - len(row))
                elif len(row) > n_cols:
                    row = row[:n_cols]
                cur.execute(insert_sql, row)
                inserted += 1
        # If there are no columns, there is nothing to insert; rows of
        # data (if any) are ignored since there is no place to put them.

        conn.commit()
        return inserted
    except ValueError:
        # Propagate contract-defined ValueErrors (e.g. table exists)
        # without wrapping, but do not leak other internals.
        raise
    except sqlite3.Error as exc:
        raise RuntimeError("Database operation failed") from exc
    finally:
        if conn is not None:
            conn.close()
