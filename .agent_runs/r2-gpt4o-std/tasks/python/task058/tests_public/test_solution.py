import csv

import pytest
from src.solution import csv_filter


def _make_csv(p, rows):
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["name", "status"])
        w.writeheader()
        w.writerows(rows)


def test_no_match(tmp_path):
    inp = tmp_path / "in.csv"
    out = tmp_path / "out.csv"
    _make_csv(inp, [{"name": "x", "status": "inactive"}])
    count = csv_filter(str(inp), str(out), "status", "active")
    assert count == 0


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


def test_header_preserved(tmp_path):
    inp = tmp_path / "in.csv"
    out = tmp_path / "out.csv"
    _make_csv(inp, [{"name": "a", "status": "active"}])
    csv_filter(str(inp), str(out), "status", "active")
    with open(out) as f:
        reader = csv.reader(f)
        header = next(reader)
    assert "name" in header and "status" in header
