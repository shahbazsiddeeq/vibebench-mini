import sqlite3

import pytest
from src.solution import upsert


def _setup_db(db_path):
    with sqlite3.connect(db_path) as conn:
        conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")


def test_update(tmp_path):
    db = str(tmp_path / "db.sqlite")
    _setup_db(db)
    upsert(db, "users", {"id": 1, "name": "Alice"}, "id")
    upsert(db, "users", {"id": 1, "name": "Bob"}, "id")
    with sqlite3.connect(db) as conn:
        rows = conn.execute("SELECT name FROM users WHERE id=1").fetchall()
    assert len(rows) == 1
    assert rows[0][0] == "Bob"


def test_update_preserves_omitted_columns(tmp_path):
    db = str(tmp_path / "db.sqlite")
    with sqlite3.connect(db) as conn:
        conn.execute(
            "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)"
        )
    upsert(db, "users", {"id": 1, "name": "Alice", "email": "a@x.com"}, "id")
    # Omit email on the update; an INSERT OR REPLACE would wipe it to NULL.
    upsert(db, "users", {"id": 1, "name": "Bob"}, "id")
    with sqlite3.connect(db) as conn:
        row = conn.execute(
            "SELECT name, email FROM users WHERE id=1"
        ).fetchone()
    assert row == ("Bob", "a@x.com")


def test_injection_in_table_raises(tmp_path):
    db = str(tmp_path / "db.sqlite")
    _setup_db(db)
    with pytest.raises(ValueError):
        upsert(db, "users; DROP TABLE users; --", {"id": 1, "name": "x"}, "id")
    with sqlite3.connect(db) as conn:
        tables = [
            r[0]
            for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        ]
    assert "users" in tables
