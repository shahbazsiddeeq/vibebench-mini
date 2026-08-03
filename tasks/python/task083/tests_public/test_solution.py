import sqlite3

import pytest
from src.solution import run_migrations


def test_multiple(tmp_path):
    db = str(tmp_path / "db.sqlite")
    migrations = [
        "CREATE TABLE a (x TEXT)",
        "CREATE TABLE b (y INTEGER)",
    ]
    count = run_migrations(db, migrations)
    assert count == 2


def test_error_raises(tmp_path):
    db = str(tmp_path / "db.sqlite")
    with pytest.raises(RuntimeError):
        run_migrations(db, ["NOT VALID SQL !!!"])


def test_error_message_contains_failing_statement(tmp_path):
    db = str(tmp_path / "db.sqlite")
    with pytest.raises(RuntimeError) as excinfo:
        run_migrations(db, ["CREATE TABLE t (id INT)", "THIS IS NOT SQL"])
    assert "THIS IS NOT SQL" in str(excinfo.value)
