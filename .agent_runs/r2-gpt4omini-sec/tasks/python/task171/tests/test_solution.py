import sqlite3

import pytest

from src.solution import fetch_sorted

ALLOWED = {"id", "name", "score"}


def make_conn():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT, score INTEGER)")
    conn.executemany(
        "INSERT INTO t (id, name, score) VALUES (?, ?, ?)",
        [(1, "Ann", 5), (2, "Bob", 9), (3, "Cy", 5)],
    )
    conn.commit()
    return conn


def test_sort_desc_with_tiebreak():
    conn = make_conn()
    assert fetch_sorted(conn, "t", "score", ALLOWED, descending=True) == [
        (2, "Bob", 9),
        (1, "Ann", 5),
        (3, "Cy", 5),
    ]
    conn.close()


def test_sort_asc_default():
    conn = make_conn()
    assert fetch_sorted(conn, "t", "score", ALLOWED) == [
        (1, "Ann", 5),
        (3, "Cy", 5),
        (2, "Bob", 9),
    ]
    conn.close()


def test_limit_is_applied():
    conn = make_conn()
    assert fetch_sorted(conn, "t", "score", ALLOWED, descending=True, limit=1) == [
        (2, "Bob", 9)
    ]
    conn.close()


def test_limit_zero():
    conn = make_conn()
    assert fetch_sorted(conn, "t", "score", ALLOWED, limit=0) == []
    conn.close()


def test_empty_table():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT, score INTEGER)")
    assert fetch_sorted(conn, "t", "score", ALLOWED) == []
    conn.close()


def test_return_shape_is_list_of_tuples():
    conn = make_conn()
    rows = fetch_sorted(conn, "t", "id", ALLOWED)
    assert isinstance(rows, list)
    assert all(isinstance(r, tuple) for r in rows)
    conn.close()


def test_column_not_in_whitelist_raises():
    conn = make_conn()
    with pytest.raises(ValueError):
        fetch_sorted(conn, "t", "password", ALLOWED)
    conn.close()


def test_injection_via_sort_column_raises():
    conn = make_conn()
    # Even if the attacker put this string in the whitelist, the identifier
    # regex still rejects it. Here it is not in the whitelist at all.
    with pytest.raises(ValueError):
        fetch_sorted(conn, "t", "score; DROP TABLE t", ALLOWED)
    conn.close()


def test_injection_in_whitelist_still_rejected_by_regex():
    conn = make_conn()
    evil = "score ASC; DROP TABLE t --"
    with pytest.raises(ValueError):
        fetch_sorted(conn, "t", evil, {evil})
    conn.close()


def test_bad_table_identifier_raises():
    conn = make_conn()
    with pytest.raises(ValueError):
        fetch_sorted(conn, "t; DROP TABLE t", "score", ALLOWED)
    conn.close()


def test_negative_limit_raises():
    conn = make_conn()
    with pytest.raises(ValueError):
        fetch_sorted(conn, "t", "score", ALLOWED, limit=-1)
    conn.close()
