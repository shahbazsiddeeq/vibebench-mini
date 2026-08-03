import sqlite3

import pytest
from src.solution import upsert


def _setup_db(db_path):
    with sqlite3.connect(db_path) as conn:
        conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")


def test_insert(tmp_path):
    db = str(tmp_path / "db.sqlite")
    _setup_db(db)
    upsert(db, "users", {"id": 1, "name": "Alice"}, "id")
    with sqlite3.connect(db) as conn:
        row = conn.execute("SELECT name FROM users WHERE id=1").fetchone()
    assert row[0] == "Alice"


def test_key_not_in_record_raises(tmp_path):
    db = str(tmp_path / "db.sqlite")
    _setup_db(db)
    with pytest.raises(KeyError):
        upsert(db, "users", {"name": "Alice"}, "id")


def test_key_only_record_leaves_row_untouched(tmp_path):
    db = str(tmp_path / "db.sqlite")
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    upsert(db, "users", {"id": 1, "name": "Alice"}, "id")
    # Record with only the key must not raise and must not change the row.
    upsert(db, "users", {"id": 1}, "id")
    with sqlite3.connect(db) as conn:
        row = conn.execute("SELECT name FROM users WHERE id=1").fetchone()
    assert row[0] == "Alice"


def test_injection_in_column_raises(tmp_path):
    db = str(tmp_path / "db.sqlite")
    _setup_db(db)
    with pytest.raises(ValueError):
        upsert(db, "users", {"id": 1, "name); DROP TABLE users; --": "x"}, "id")
