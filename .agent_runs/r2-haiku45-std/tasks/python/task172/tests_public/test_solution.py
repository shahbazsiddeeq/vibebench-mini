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


def test_count():
    conn = make_conn()
    assert group_aggregate(conn, "sales", "region", "amount", "COUNT") == [
        (None, 1),
        ("E", 2),
        ("W", 1),
    ]
    conn.close()


def test_avg_is_float():
    conn = make_conn()
    assert group_aggregate(conn, "sales", "region", "amount", "AVG") == [
        (None, 7.0),
        ("E", 7.5),
        ("W", 3.0),
    ]
    conn.close()


def test_empty_table():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE sales (region TEXT, amount INTEGER)")
    assert group_aggregate(conn, "sales", "region", "amount", "SUM") == []
    conn.close()


def test_bad_aggregate_raises():
    conn = make_conn()
    with pytest.raises(ValueError):
        group_aggregate(conn, "sales", "region", "amount", "DROP")
    conn.close()


def test_bad_group_identifier_raises():
    conn = make_conn()
    with pytest.raises(ValueError):
        group_aggregate(conn, "sales", "region); DROP TABLE sales --", "amount", "SUM")
    conn.close()
