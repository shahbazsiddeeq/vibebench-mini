import sqlite3

import pytest
from src.solution import batch_insert


def _setup(db):
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE items (name TEXT, val INTEGER)")


def test_basic(tmp_path):
    db = str(tmp_path / "db.sqlite")
    _setup(db)
    count = batch_insert(
        db, "items", [{"name": "a", "val": 1}, {"name": "b", "val": 2}]
    )
    assert count == 2


def test_empty_rows(tmp_path):
    db = str(tmp_path / "db.sqlite")
    _setup(db)
    assert batch_insert(db, "items", []) == 0


def test_mid_batch_failure_rolls_back(tmp_path):
    db = str(tmp_path / "db.sqlite")
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE items (name TEXT PRIMARY KEY, val INTEGER)")
    rows = [
        {"name": "a", "val": 1},
        {"name": "b", "val": 2},
        {"name": "a", "val": 3},  # duplicate PK -> fails mid-batch
    ]
    with pytest.raises(RuntimeError):
        batch_insert(db, "items", rows)
    # Whole batch must roll back; a per-row autocommit version leaves a and b.
    with sqlite3.connect(db) as conn:
        count = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    assert count == 0


def test_injection_in_table_raises(tmp_path):
    db = str(tmp_path / "db.sqlite")
    _setup(db)
    with pytest.raises(ValueError):
        batch_insert(db, "items; DROP TABLE items; --", [{"name": "a", "val": 1}])
    with sqlite3.connect(db) as conn:
        tables = [
            r[0]
            for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        ]
    assert "items" in tables
