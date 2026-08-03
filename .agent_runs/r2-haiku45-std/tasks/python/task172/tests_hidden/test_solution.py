import sqlite3

import pytest

from src.solution import group_aggregate


def make_conn():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE sales (region TEXT, amount INTEGER)")
    conn.executemany(
        "INSERT INTO sales (region, amount) VALUES (?, ?)",
        [("E", 10), ("E", 5), ("W", 3), (None, 7)],
    )
    conn.commit()
    return conn


def test_sum_with_null_group_first():
    conn = make_conn()
    assert group_aggregate(conn, "sales", "region", "amount", "SUM") == [
        (None, 7),
        ("E", 15),
        ("W", 3),
    ]
    conn.close()


def test_max_and_min():
    conn = make_conn()
    assert group_aggregate(conn, "sales", "region", "amount", "MAX") == [
        (None, 7),
        ("E", 10),
        ("W", 3),
    ]
    assert group_aggregate(conn, "sales", "region", "amount", "MIN") == [
        (None, 7),
        ("E", 5),
        ("W", 3),
    ]
    conn.close()


def test_agg_is_case_insensitive():
    conn = make_conn()
    assert group_aggregate(conn, "sales", "region", "amount", "sum") == [
        (None, 7),
        ("E", 15),
        ("W", 3),
    ]
    conn.close()


def test_return_shape_is_list_of_two_tuples():
    conn = make_conn()
    rows = group_aggregate(conn, "sales", "region", "amount")
    assert isinstance(rows, list)
    assert all(isinstance(r, tuple) and len(r) == 2 for r in rows)
    conn.close()


def test_injection_via_aggregate_raises():
    conn = make_conn()
    with pytest.raises(ValueError):
        group_aggregate(conn, "sales", "region", "amount", "SUM(amount)); DROP TABLE sales --")
    conn.close()
