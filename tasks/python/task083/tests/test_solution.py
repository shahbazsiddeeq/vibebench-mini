import sqlite3

import pytest
from src.solution import run_migrations


def test_basic(tmp_path):
    db = str(tmp_path / "db.sqlite")
    count = run_migrations(db, ["CREATE TABLE t (id INTEGER PRIMARY KEY)"])
    assert count == 1


def test_multiple(tmp_path):
    db = str(tmp_path / "db.sqlite")
    migrations = [
        "CREATE TABLE a (x TEXT)",
        "CREATE TABLE b (y INTEGER)",
    ]
    count = run_migrations(db, migrations)
    assert count == 2


def test_empty_list(tmp_path):
    db = str(tmp_path / "db.sqlite")
    assert run_migrations(db, []) == 0


def test_error_raises(tmp_path):
    db = str(tmp_path / "db.sqlite")
    with pytest.raises(RuntimeError):
        run_migrations(db, ["NOT VALID SQL !!!"])


def test_tables_persist_from_fresh_connection(tmp_path):
    db = str(tmp_path / "db.sqlite")
    run_migrations(
        db,
        [
            "CREATE TABLE a (x TEXT)",
            "CREATE TABLE b (y INTEGER)",
            "INSERT INTO a VALUES ('hello')",
        ],
    )
    # A runner that never commits would show nothing on a brand-new connection.
    with sqlite3.connect(db) as conn:
        tables = {
            r[0]
            for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
        assert {"a", "b"} <= tables
        assert conn.execute("SELECT x FROM a").fetchone()[0] == "hello"


def test_error_message_contains_failing_statement(tmp_path):
    db = str(tmp_path / "db.sqlite")
    with pytest.raises(RuntimeError) as excinfo:
        run_migrations(db, ["CREATE TABLE t (id INT)", "THIS IS NOT SQL"])
    assert "THIS IS NOT SQL" in str(excinfo.value)


def test_rollback_on_error(tmp_path):
    db = str(tmp_path / "db.sqlite")
    try:
        run_migrations(db, ["CREATE TABLE t (x INT)", "BAD SQL"])
    except RuntimeError:
        pass
    with sqlite3.connect(db) as conn:
        tables = [
            r[0]
            for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        ]
    assert "t" not in tables
