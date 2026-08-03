import sqlite3

import pytest

from src.solution import transfer


def make_conn():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE accounts (acct INTEGER PRIMARY KEY, bal INTEGER)")
    conn.executemany(
        "INSERT INTO accounts (acct, bal) VALUES (?, ?)",
        [(1, 100), (2, 50)],
    )
    conn.commit()
    return conn


def balances(conn):
    rows = conn.execute("SELECT acct, bal FROM accounts ORDER BY acct").fetchall()
    return dict(rows)


def test_successful_transfer_persists():
    conn = make_conn()
    transfer(conn, "accounts", "acct", "bal", 1, 2, 30)
    assert balances(conn) == {1: 70, 2: 80}
    conn.close()


def test_account_not_found_rolls_back():
    conn = make_conn()
    with pytest.raises(ValueError, match="account not found"):
        transfer(conn, "accounts", "acct", "bal", 1, 99, 10)
    assert balances(conn) == {1: 100, 2: 50}
    conn.close()


def test_zero_amount_raises():
    conn = make_conn()
    with pytest.raises(ValueError):
        transfer(conn, "accounts", "acct", "bal", 1, 2, 0)
    assert balances(conn) == {1: 100, 2: 50}
    conn.close()


def test_bool_amount_rejected():
    conn = make_conn()
    with pytest.raises(ValueError):
        transfer(conn, "accounts", "acct", "bal", 1, 2, True)
    assert balances(conn) == {1: 100, 2: 50}
    conn.close()


def test_same_account_raises():
    conn = make_conn()
    with pytest.raises(ValueError):
        transfer(conn, "accounts", "acct", "bal", 1, 1, 10)
    conn.close()


def test_bad_column_identifier_raises():
    conn = make_conn()
    with pytest.raises(ValueError):
        transfer(conn, "accounts", "acct", "bal = 0 --", 1, 2, 10)
    conn.close()


def test_return_shape_is_tuple_of_ints():
    conn = make_conn()
    result = transfer(conn, "accounts", "acct", "bal", 1, 2, 30)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(x, int) for x in result)
    conn.close()
