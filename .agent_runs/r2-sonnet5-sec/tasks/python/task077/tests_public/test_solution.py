import csv
import sqlite3

import pytest
from src.solution import csv_to_sqlite


def _make_csv(p, rows, header):
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        w.writerows(rows)


def test_data_queryable(tmp_path):
    csv_p = str(tmp_path / "data.csv")
    db_p = str(tmp_path / "out.db")
    _make_csv(csv_p, [{"x": "hello"}], ["x"])
    csv_to_sqlite(csv_p, db_p, "t")
    with sqlite3.connect(db_p) as conn:
        row = conn.execute("SELECT x FROM t").fetchone()
    assert row[0] == "hello"


def test_columns_are_all_text(tmp_path):
    csv_p = str(tmp_path / "data.csv")
    db_p = str(tmp_path / "out.db")
    _make_csv(csv_p, [{"a": "1", "b": "hi"}], ["a", "b"])
    csv_to_sqlite(csv_p, db_p, "t")
    with sqlite3.connect(db_p) as conn:
        types = {r[1]: r[2] for r in conn.execute("PRAGMA table_info(t)")}
    assert types == {"a": "TEXT", "b": "TEXT"}


def test_invalid_table_name_raises(tmp_path):
    csv_p = str(tmp_path / "data.csv")
    db_p = str(tmp_path / "out.db")
    _make_csv(csv_p, [{"x": "1"}], ["x"])
    with pytest.raises(ValueError):
        csv_to_sqlite(csv_p, db_p, "bad-name!")
