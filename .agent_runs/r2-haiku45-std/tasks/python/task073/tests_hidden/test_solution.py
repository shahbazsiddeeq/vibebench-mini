import sqlite3

import pytest
from src.solution import create_table


def test_creates_table(tmp_path):
    db = str(tmp_path / "db.sqlite")
    create_table(db, "users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
    with sqlite3.connect(db) as conn:
        tables = [
            r[0]
            for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        ]
    assert "users" in tables


def test_already_exists_raises(tmp_path):
    db = str(tmp_path / "db.sqlite")
    create_table(db, "t", {"id": "INTEGER"})
    with pytest.raises(ValueError):
        create_table(db, "t", {"id": "INTEGER"})


def test_case_insensitive_duplicate_raises_valueerror(tmp_path):
    db = str(tmp_path / "db.sqlite")
    create_table(db, "t", {"id": "INTEGER"})
    with pytest.raises(ValueError):
        create_table(db, "T", {"id": "INTEGER"})


def test_injection_in_type_raises(tmp_path):
    db = str(tmp_path / "db.sqlite")
    with pytest.raises(ValueError):
        create_table(db, "safe", {"id": "INTEGER); DROP TABLE users; --"})
