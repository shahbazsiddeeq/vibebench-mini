import sqlite3

import pytest
from src.solution import value_counts


def _make_db(tmp_path, values):
    db = str(tmp_path / "db.sqlite")
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE t (color TEXT)")
        conn.executemany("INSERT INTO t VALUES (?)", [(v,) for v in values])
    return db


def test_single_value(tmp_path):
    db = _make_db(tmp_path, ["green", "green", "green"])
    assert value_counts(db, "t", "color") == {"green": 3}


def test_empty_table(tmp_path):
    db = _make_db(tmp_path, [])
    assert value_counts(db, "t", "color") == {}


def test_invalid_table_raises(tmp_path):
    db = _make_db(tmp_path, ["red"])
    with pytest.raises(ValueError):
        value_counts(db, "bad-name!", "color")
