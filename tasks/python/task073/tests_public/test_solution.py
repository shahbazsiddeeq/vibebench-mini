import sqlite3

import pytest
from src.solution import create_table


def test_columns_created(tmp_path):
    db = str(tmp_path / "db.sqlite")
    create_table(db, "items", {"x": "INTEGER", "y": "TEXT"})
    with sqlite3.connect(db) as conn:
        conn.execute("INSERT INTO items VALUES (1, 'hello')")


def test_invalid_name_raises(tmp_path):
    db = str(tmp_path / "db.sqlite")
    with pytest.raises(ValueError):
        create_table(db, "bad-name!", {"id": "INTEGER"})


def test_injection_in_column_name_raises(tmp_path):
    db = str(tmp_path / "db.sqlite")
    with pytest.raises(ValueError):
        create_table(
            db,
            "safe",
            {"x INTEGER); DROP TABLE users; --": "INTEGER"},
        )
    # The malicious statement must not have created anything.
    with sqlite3.connect(db) as conn:
        tables = [
            r[0]
            for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        ]
    assert "safe" not in tables


def test_quoted_identifier_column_created(tmp_path):
    db = str(tmp_path / "db.sqlite")
    # A column name that is a SQL keyword must still work thanks to quoting.
    create_table(db, "kw", {"select": "TEXT", "from": "INTEGER"})
    with sqlite3.connect(db) as conn:
        conn.execute('INSERT INTO kw ("select", "from") VALUES (?, ?)', ("a", 1))
        row = conn.execute('SELECT "select", "from" FROM kw').fetchone()
    assert row == ("a", 1)
