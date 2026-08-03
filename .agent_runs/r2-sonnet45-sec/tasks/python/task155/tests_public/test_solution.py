import pytest

from src.solution import group_by_aggregate


def test_empty_returns_empty_dict():
    assert group_by_aggregate([], "d", "v") == {}


def test_sums_and_means_are_floats():
    out = group_by_aggregate([{"k": "x", "n": 4}], "k", "n")
    assert isinstance(out["x"]["sum"], float)
    assert isinstance(out["x"]["mean"], float)
    assert isinstance(out["x"]["count"], int)


def test_missing_field_raises_keyerror():
    with pytest.raises(KeyError):
        group_by_aggregate([{"k": "x"}], "k", "n")


def test_mean_divides_by_count_not_group_total():
    records = [{"k": "a", "n": 2}, {"k": "a", "n": 4}]
    assert group_by_aggregate(records, "k", "n")["a"]["mean"] == 3.0
