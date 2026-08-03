import sqlite3

import pytest
from src.solution import batch_insert


def _setup(db):
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE items (name TEXT, val INTEGER)")


def test_data_inserted(tmp_path):
    db = str(tmp_path / "db.sqlite")
    _setup(db)
    batch_insert(db, "items", [{"name": "x", "val": 99}])
    with sqlite3.connect(db) as conn:
        row = conn.execute("SELECT val FROM items WHERE name='x'").fetchone()
    assert row[0] == 99


def test_error_raises(tmp_path):
    db = str(tmp_path / "db.sqlite")
    _setup(db)
    with pytest.raises(RuntimeError):
        batch_insert(db, "nonexistent_table", [{"x": 1}])


def test_mismatched_row_keys_raise_runtimeerror(tmp_path):
    db = str(tmp_path / "db.sqlite")
    _setup(db)
    rows = [{"name": "a", "val": 1}, {"name": "b"}]  # second row missing 'val'
    with pytest.raises(RuntimeError):
        batch_insert(db, "items", rows)
    with sqlite3.connect(db) as conn:
        count = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    assert count == 0


def test_injection_in_column_raises(tmp_path):
    db = str(tmp_path / "db.sqlite")
    _setup(db)
    with pytest.raises(ValueError):
        batch_insert(db, "items", [{"name); DROP TABLE items; --": "a"}])
