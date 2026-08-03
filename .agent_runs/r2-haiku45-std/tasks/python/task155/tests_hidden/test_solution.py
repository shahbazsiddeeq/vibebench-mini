import pytest

from src.solution import group_by_aggregate


def test_worked_example():
    records = [
        {"d": "A", "v": 100},
        {"d": "A", "v": 200},
        {"d": "B", "v": 50},
        {"d": "A", "v": 1},
    ]
    assert group_by_aggregate(records, "d", "v") == {
        "A": {"count": 3, "sum": 301.0, "mean": 100.3333},
        "B": {"count": 1, "sum": 50.0, "mean": 50.0},
    }


def test_single_record():
    assert group_by_aggregate([{"k": "x", "n": 7}], "k", "n") == {
        "x": {"count": 1, "sum": 7.0, "mean": 7.0}
    }


def test_negatives():
    records = [{"k": "g", "n": -5}, {"k": "g", "n": 5}, {"k": "g", "n": -10}]
    assert group_by_aggregate(records, "k", "n") == {
        "g": {"count": 3, "sum": -10.0, "mean": -3.3333}
    }


def test_rounding_is_enforced():
    # 1/3 = 0.33333... An implementation that skips rounding to 4 places fails.
    records = [{"k": "a", "n": 0}, {"k": "a", "n": 0}, {"k": "a", "n": 1}]
    out = group_by_aggregate(records, "k", "n")
    assert out["a"]["mean"] == 0.3333
