import pytest
from src.solution import percentile


def test_p50_matches_median():
    data = [1, 2, 3, 4, 5]
    assert percentile(data, 50) == 3.0


def test_p100_is_max():
    assert percentile([1, 2, 3], 100) == 3


def test_p_below_zero_raises():
    with pytest.raises(ValueError):
        percentile([1, 2], -1)


def test_interpolation():
    result = percentile([1, 3], 50)
    assert result == 2.0


def test_single_element():
    assert percentile([42], 0) == 42.0
    assert percentile([42], 50) == 42.0
    assert percentile([42], 100) == 42.0
