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


def test_empty_filters_returns_all_ordered():
    conn = make_conn()
    assert select_where(conn, "t", {}) == [
        (1, "Ann", 30),
        (2, "Bob", 30),
        (3, "Cy", 40),
        (4, "Dan", None),
    ]
    conn.close()


def test_multiple_filters_and():
    conn = make_conn()
    assert select_where(conn, "t", {"age": 30, "name": "Bob"}) == [(2, "Bob", 30)]
    conn.close()


def test_no_match_returns_empty():
    conn = make_conn()
    assert select_where(conn, "t", {"age": 99}) == []
    conn.close()


def test_none_matches_null():
    conn = make_conn()
    assert select_where(conn, "t", {"age": None}) == [(4, "Dan", None)]
    conn.close()


def test_value_is_bound_not_injected():
    conn = make_conn()
    # A malicious VALUE must be safely bound and simply match nothing.
    assert select_where(conn, "t", {"name": "x'; DROP TABLE t; --"}) == []
    # Table still exists / still has all rows.
    assert len(select_where(conn, "t", {})) == 4
    conn.close()


def test_return_shape_is_list_of_tuples():
    conn = make_conn()
    rows = select_where(conn, "t", {"age": 30})
    assert isinstance(rows, list)
    assert all(isinstance(r, tuple) for r in rows)
    conn.close()


def test_bad_table_identifier_raises():
    conn = make_conn()
    with pytest.raises(ValueError):
        select_where(conn, "t; DROP TABLE t", {})
    conn.close()


def test_bad_column_identifier_raises():
    conn = make_conn()
    with pytest.raises(ValueError):
        select_where(conn, "t", {"age = 30 OR 1=1 --": 1})
    conn.close()
