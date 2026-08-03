import re
import sqlite3

_IDENTIFIER_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')


def _validate_identifier(name):
    if not isinstance(name, str) or not _IDENTIFIER_RE.match(name):
        raise ValueError(f"Invalid identifier: {name!r}")


def value_counts(db_path, table, column):
    _validate_identifier(table)
    _validate_identifier(column)

    query = f'SELECT "{column}", COUNT(*) FROM "{table}" GROUP BY "{column}"'

    result = {}
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(query)
        for value, count in cursor.fetchall():
            result[value] = count

    return result
