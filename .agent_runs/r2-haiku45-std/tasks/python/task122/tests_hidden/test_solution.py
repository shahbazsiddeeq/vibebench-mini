import sqlite3

import pytest
from src.solution import value_counts


def _make_db(tmp_path, values):
    db = str(tmp_path / "db.sqlite")
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE t (color TEXT)")
        conn.executemany("INSERT INTO t VALUES (?)", [(v,) for v in values])
    return db


def test_basic_counts(tmp_path):
    db = _make_db(tmp_path, ["red", "red", "blue"])
    assert value_counts(db, "t", "color") == {"red": 2, "blue": 1}


def test_all_distinct(tmp_path):
    db = _make_db(tmp_path, ["a", "b", "c"])
    assert value_counts(db, "t", "color") == {"a": 1, "b": 1, "c": 1}


def test_counts_include_null(tmp_path):
    db = _make_db(tmp_path, ["red", None, None])
    assert value_counts(db, "t", "color") == {"red": 1, None: 2}


def test_invalid_column_raises(tmp_path):
    db = _make_db(tmp_path, ["red"])
    with pytest.raises(ValueError):
        value_counts(db, "t", "bad-col!")
