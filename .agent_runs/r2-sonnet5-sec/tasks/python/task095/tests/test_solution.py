import pytest
from src.solution import percentile


def test_p50_matches_median():
    data = [1, 2, 3, 4, 5]
    assert percentile(data, 50) == 3.0


def test_p0_is_min():
    assert percentile([1, 2, 3], 0) == 1


def test_p100_is_max():
    assert percentile([1, 2, 3], 100) == 3


def test_empty_raises():
    with pytest.raises(ValueError):
        percentile([], 50)


def test_p_below_zero_raises():
    with pytest.raises(ValueError):
        percentile([1, 2], -1)


def test_p_above_100_raises():
    with pytest.raises(ValueError):
        percentile([1, 2], 101)


def test_interpolation():
    result = percentile([1, 3], 50)
    assert result == 2.0


def test_unsorted_input():
    # A solution that skips sorting would return a different value here.
    assert percentile([3, 1, 2], 50) == 2.0
    assert percentile([4, 1, 3, 2], 25) == 1.75


def test_single_element():
    assert percentile([42], 0) == 42.0
    assert percentile([42], 50) == 42.0
    assert percentile([42], 100) == 42.0
