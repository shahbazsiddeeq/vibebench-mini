import sqlite3

import pytest
from src.solution import paginate


def _make_db(tmp_path, n):
    db = str(tmp_path / "db.sqlite")
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE t (id INTEGER, name TEXT)")
        conn.executemany(
            "INSERT INTO t VALUES (?, ?)",
            [(i, f"row{i}") for i in range(1, n + 1)],
        )
    return db


def test_first_page(tmp_path):
    db = _make_db(tmp_path, 5)
    rows = paginate(db, "t", 1, 3)
    assert rows == [(1, "row1"), (2, "row2"), (3, "row3")]


def test_page_past_end_is_empty(tmp_path):
    db = _make_db(tmp_path, 5)
    assert paginate(db, "t", 10, 2) == []


def test_page_below_one_raises(tmp_path):
    db = _make_db(tmp_path, 5)
    with pytest.raises(ValueError):
        paginate(db, "t", 0, 2)


def test_returns_plain_tuples(tmp_path):
    db = _make_db(tmp_path, 3)
    rows = paginate(db, "t", 1, 3)
    assert all(type(r) is tuple for r in rows)
    assert rows == [(1, "row1"), (2, "row2"), (3, "row3")]
