import sqlite3

import pytest

from src.solution import bulk_update


def make_conn():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    conn.executemany(
        "INSERT INTO users (id, name, age) VALUES (?, ?, ?)",
        [(1, "Ann", 30), (2, "Bob", 25), (3, "Cy", 40)],
    )
    conn.commit()
    return conn


def snapshot(conn):
    return conn.execute("SELECT id, name, age FROM users ORDER BY id").fetchall()


def test_returns_total_rows_modified():
    conn = make_conn()
    n = bulk_update(
        conn, "users", "id", [{"id": 1, "age": 31}, {"id": 2, "name": "Bobby", "age": 26}]
    )
    assert n == 2
    conn.close()


def test_multiple_columns_single_row():
    conn = make_conn()
    n = bulk_update(conn, "users", "id", [{"id": 3, "name": "Cyrus", "age": 41}])
    assert n == 1
    assert snapshot(conn)[2] == (3, "Cyrus", 41)
    conn.close()


def test_non_matching_key_counts_zero():
    conn = make_conn()
    # id 99 matches nothing -> rowcount 0; id 1 matches -> 1.
    n = bulk_update(conn, "users", "id", [{"id": 99, "age": 5}, {"id": 1, "age": 33}])
    assert n == 1
    assert snapshot(conn)[0] == (1, "Ann", 33)
    conn.close()


def test_injected_column_identifier_raises():
    conn = make_conn()
    with pytest.raises(ValueError):
        bulk_update(conn, "users", "id", [{"id": 1, "age = 0 --": 5}])
    # Nothing changed.
    assert snapshot(conn) == [(1, "Ann", 30), (2, "Bob", 25), (3, "Cy", 40)]
    conn.close()


def test_bad_key_column_identifier_raises():
    conn = make_conn()
    with pytest.raises(ValueError):
        bulk_update(conn, "users", "id = 1 OR 1=1", [{"id = 1 OR 1=1": 1, "age": 5}])
    conn.close()


def test_no_columns_to_update_raises():
    conn = make_conn()
    with pytest.raises(ValueError):
        bulk_update(conn, "users", "id", [{"id": 1}])
    conn.close()


def test_batch_rolls_back_on_bad_row():
    conn = make_conn()
    # First row is valid, second row has an invalid identifier: whole batch
    # must be rejected before any change is applied.
    with pytest.raises(ValueError):
        bulk_update(
            conn, "users", "id", [{"id": 1, "age": 99}, {"id": 2, "bad col": 1}]
        )
    assert snapshot(conn) == [(1, "Ann", 30), (2, "Bob", 25), (3, "Cy", 40)]
    conn.close()


def test_connection_not_closed():
    conn = make_conn()
    bulk_update(conn, "users", "id", [{"id": 1, "age": 31}])
    assert conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 3
    conn.close()
