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


def test_second_page(tmp_path):
    db = _make_db(tmp_path, 5)
    rows = paginate(db, "t", 2, 2)
    assert rows == [(3, "row3"), (4, "row4")]


def test_last_partial_page(tmp_path):
    db = _make_db(tmp_path, 5)
    rows = paginate(db, "t", 3, 2)
    assert rows == [(5, "row5")]


def test_invalid_table_raises(tmp_path):
    db = _make_db(tmp_path, 5)
    with pytest.raises(ValueError):
        paginate(db, "bad-name!", 1, 2)


def test_page_size_below_one_raises(tmp_path):
    db = _make_db(tmp_path, 5)
    with pytest.raises(ValueError):
        paginate(db, "t", 1, 0)


def test_ordered_by_rowid_not_column_value(tmp_path):
    db = str(tmp_path / "db.sqlite")
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE t (id INTEGER, name TEXT)")
        # Insertion (rowid) order differs from ascending id order.
        conn.executemany(
            "INSERT INTO t VALUES (?, ?)",
            [(5, "e"), (3, "c"), (1, "a")],
        )
    # Must be returned in rowid/insertion order, not sorted by id.
    assert paginate(db, "t", 1, 3) == [(5, "e"), (3, "c"), (1, "a")]
    assert paginate(db, "t", 1, 2) == [(5, "e"), (3, "c")]
    assert paginate(db, "t", 2, 2) == [(1, "a")]
