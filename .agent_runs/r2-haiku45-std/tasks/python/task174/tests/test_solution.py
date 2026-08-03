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


def test_updates_persist():
    conn = make_conn()
    bulk_update(
        conn, "users", "id", [{"id": 1, "age": 31}, {"id": 2, "name": "Bobby", "age": 26}]
    )
    assert snapshot(conn) == [(1, "Ann", 31), (2, "Bobby", 26), (3, "Cy", 40)]
    conn.close()


def test_multiple_columns_single_row():
    conn = make_conn()
    n = bulk_update(conn, "users", "id", [{"id": 3, "name": "Cyrus", "age": 41}])
    assert n == 1
    assert snapshot(conn)[2] == (3, "Cyrus", 41)
    conn.close()


def test_empty_rows_returns_zero_no_change():
    conn = make_conn()
    assert bulk_update(conn, "users", "id", []) == 0
    assert snapshot(conn) == [(1, "Ann", 30), (2, "Bob", 25), (3, "Cy", 40)]
    conn.close()


def test_non_matching_key_counts_zero():
    conn = make_conn()
    # id 99 matches nothing -> rowcount 0; id 1 matches -> 1.
    n = bulk_update(conn, "users", "id", [{"id": 99, "age": 5}, {"id": 1, "age": 33}])
    assert n == 1
    assert snapshot(conn)[0] == (1, "Ann", 33)
    conn.close()


def test_values_are_bound_not_injected():
    conn = make_conn()
    # A malicious VALUE is safely bound as text, not executed.
    n = bulk_update(conn, "users", "id", [{"id": 1, "name": "x'; DROP TABLE users; --"}])
    assert n == 1
    # Table intact and value stored literally.
    assert snapshot(conn)[0] == (1, "x'; DROP TABLE users; --", 30)
    assert len(snapshot(conn)) == 3
    conn.close()


def test_injected_column_identifier_raises():
    conn = make_conn()
    with pytest.raises(ValueError):
        bulk_update(conn, "users", "id", [{"id": 1, "age = 0 --": 5}])
    # Nothing changed.
    assert snapshot(conn) == [(1, "Ann", 30), (2, "Bob", 25), (3, "Cy", 40)]
    conn.close()


def test_bad_table_identifier_raises():
    conn = make_conn()
    with pytest.raises(ValueError):
        bulk_update(conn, "users; DROP TABLE users", "id", [{"id": 1, "age": 5}])
    assert len(snapshot(conn)) == 3
    conn.close()


def test_bad_key_column_identifier_raises():
    conn = make_conn()
    with pytest.raises(ValueError):
        bulk_update(conn, "users", "id = 1 OR 1=1", [{"id = 1 OR 1=1": 1, "age": 5}])
    conn.close()


def test_missing_key_column_raises():
    conn = make_conn()
    with pytest.raises(ValueError):
        bulk_update(conn, "users", "id", [{"age": 31}])
    conn.close()


def test_no_columns_to_update_raises():
    conn = make_conn()
    with pytest.raises(ValueError):
        bulk_update(conn, "users", "id", [{"id": 1}])
    conn.close()


def test_rows_not_a_list_raises():
    conn = make_conn()
    with pytest.raises(ValueError):
        bulk_update(conn, "users", "id", {"id": 1, "age": 5})
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


def test_return_type_is_int():
    conn = make_conn()
    result = bulk_update(conn, "users", "id", [{"id": 1, "age": 31}])
    assert isinstance(result, int)
    conn.close()


def test_connection_not_closed():
    conn = make_conn()
    bulk_update(conn, "users", "id", [{"id": 1, "age": 31}])
    assert conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 3
    conn.close()
