import sqlite3

import pytest

from src.solution import select_where


def make_conn():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    conn.executemany(
        "INSERT INTO t (id, name, age) VALUES (?, ?, ?)",
        [(1, "Ann", 30), (2, "Bob", 30), (3, "Cy", 40), (4, "Dan", None)],
    )
    conn.commit()
    return conn


def test_single_filter():
    conn = make_conn()
    assert select_where(conn, "t", {"age": 30}) == [(1, "Ann", 30), (2, "Bob", 30)]
    conn.close()


def test_multiple_filters_and():
    conn = make_conn()
    assert select_where(conn, "t", {"age": 30, "name": "Bob"}) == [(2, "Bob", 30)]
    conn.close()


def test_none_matches_null():
    conn = make_conn()
    assert select_where(conn, "t", {"age": None}) == [(4, "Dan", None)]
    conn.close()


def test_return_shape_is_list_of_tuples():
    conn = make_conn()
    rows = select_where(conn, "t", {"age": 30})
    assert isinstance(rows, list)
    assert all(isinstance(r, tuple) for r in rows)
    conn.close()


def test_bad_column_identifier_raises():
    conn = make_conn()
    with pytest.raises(ValueError):
        select_where(conn, "t", {"age = 30 OR 1=1 --": 1})
    conn.close()
