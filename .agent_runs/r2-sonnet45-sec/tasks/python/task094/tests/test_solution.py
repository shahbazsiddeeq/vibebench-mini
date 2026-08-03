import pytest
from src.solution import describe


def test_basic():
    result = describe([1, 2, 3, 4, 5])
    assert result["count"] == 5
    assert result["mean"] == 3.0
    assert result["min"] == 1
    assert result["max"] == 5


def test_empty_raises():
    with pytest.raises(ValueError):
        describe([])


def test_single_element():
    result = describe([42.0])
    assert result["mean"] == 42.0
    assert result["std_dev"] == 0.0


def test_range():
    result = describe([1, 5])
    assert result["range"] == 4


def test_median_odd():
    result = describe([1, 2, 3])
    assert result["median"] == 2.0


def test_std_dev_nonnegative():
    result = describe([1, 2, 3, 4, 5])
    assert result["std_dev"] >= 0


def test_mode_none_when_all_distinct():
    result = describe([1, 2, 3, 4, 5])
    assert result["mode"] is None


def test_mode_most_frequent():
    result = describe([1, 2, 2, 3, 3, 3])
    assert result["mode"] == 3


def test_mode_ties_pick_smallest():
    result = describe([4, 4, 1, 1, 2])
    assert result["mode"] == 1


def test_population_std_dev_rounded():
    result = describe([1, 2, 2, 3])
    assert result["std_dev"] == 0.7071


def test_rounding_to_4dp():
    result = describe([1, 2, 3, 3])
    assert result["mean"] == 2.25
    assert result["std_dev"] == 0.8292
