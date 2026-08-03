import csv
import sqlite3

import pytest
from src.solution import csv_to_sqlite


def _make_csv(p, rows, header):
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        w.writerows(rows)


def test_basic(tmp_path):
    csv_p = str(tmp_path / "data.csv")
    db_p = str(tmp_path / "out.db")
    _make_csv(
        csv_p, [{"name": "a", "val": "1"}, {"name": "b", "val": "2"}], ["name", "val"]
    )
    count = csv_to_sqlite(csv_p, db_p, "items")
    assert count == 2


def test_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        csv_to_sqlite(str(tmp_path / "nope.csv"), str(tmp_path / "db.sqlite"), "t")


def test_quote_in_header_raises(tmp_path):
    csv_p = str(tmp_path / "data.csv")
    db_p = str(tmp_path / "out.db")
    # Header carrying a quote/paren that would break out of a naive DDL.
    with open(csv_p, "w", newline="") as f:
        f.write('"x"" TEXT); DROP TABLE t; --",y\n')
        f.write("1,2\n")
    with pytest.raises(ValueError):
        csv_to_sqlite(csv_p, db_p, "t")


def test_existing_table_raises_no_duplicate_append(tmp_path):
    csv_p = str(tmp_path / "data.csv")
    db_p = str(tmp_path / "out.db")
    _make_csv(csv_p, [{"x": "1"}, {"x": "2"}], ["x"])
    assert csv_to_sqlite(csv_p, db_p, "t") == 2
    with pytest.raises(ValueError):
        csv_to_sqlite(csv_p, db_p, "t")
    # Re-import must not have appended duplicate rows.
    with sqlite3.connect(db_p) as conn:
        n = conn.execute("SELECT COUNT(*) FROM t").fetchone()[0]
    assert n == 2
