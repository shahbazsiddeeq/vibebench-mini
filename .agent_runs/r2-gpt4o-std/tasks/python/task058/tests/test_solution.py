import csv

import pytest
from src.solution import csv_filter


def _make_csv(p, rows):
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["name", "status"])
        w.writeheader()
        w.writerows(rows)


def test_basic_filter(tmp_path):
    inp = tmp_path / "in.csv"
    out = tmp_path / "out.csv"
    _make_csv(
        inp, [{"name": "a", "status": "active"}, {"name": "b", "status": "inactive"}]
    )
    count = csv_filter(str(inp), str(out), "status", "active")
    assert count == 1
    with open(out) as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["name"] == "a"


def test_no_match(tmp_path):
    inp = tmp_path / "in.csv"
    out = tmp_path / "out.csv"
    _make_csv(inp, [{"name": "x", "status": "inactive"}])
    count = csv_filter(str(inp), str(out), "status", "active")
    assert count == 0


def test_multi_match(tmp_path):
    inp = tmp_path / "in.csv"
    out = tmp_path / "out.csv"
    _make_csv(
        inp,
        [
            {"name": "a", "status": "active"},
            {"name": "b", "status": "inactive"},
            {"name": "c", "status": "active"},
            {"name": "d", "status": "active"},
        ],
    )
    count = csv_filter(str(inp), str(out), "status", "active")
    assert count == 3
    with open(out, newline="") as f:
        rows = list(csv.DictReader(f))
    assert [r["name"] for r in rows] == ["a", "c", "d"]
    assert all(r["status"] == "active" for r in rows)


def test_quoted_fields_preserved(tmp_path):
    inp = tmp_path / "in.csv"
    out = tmp_path / "out.csv"
    _make_csv(
        inp,
        [
            {"name": "Doe, John", "status": "active"},
            {"name": 'quote"d', "status": "active"},
            {"name": "skip", "status": "inactive"},
        ],
    )
    count = csv_filter(str(inp), str(out), "status", "active")
    assert count == 2
    with open(out, newline="") as f:
        rows = list(csv.DictReader(f))
    assert [r["name"] for r in rows] == ["Doe, John", 'quote"d']


def test_missing_column_raises(tmp_path):
    inp = tmp_path / "in.csv"
    out = tmp_path / "out.csv"
    _make_csv(inp, [{"name": "a", "status": "active"}])
    with pytest.raises(KeyError):
        csv_filter(str(inp), str(out), "missing_col", "x")


def test_header_preserved(tmp_path):
    inp = tmp_path / "in.csv"
    out = tmp_path / "out.csv"
    _make_csv(inp, [{"name": "a", "status": "active"}])
    csv_filter(str(inp), str(out), "status", "active")
    with open(out) as f:
        reader = csv.reader(f)
        header = next(reader)
    assert "name" in header and "status" in header
