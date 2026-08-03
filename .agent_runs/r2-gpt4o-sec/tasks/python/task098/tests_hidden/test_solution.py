import pytest
from src.solution import pearson_r


def test_perfect_positive():
    assert abs(pearson_r([1, 2, 3], [1, 2, 3]) - 1.0) < 1e-9


def test_no_correlation():
    with pytest.raises(ValueError):
        pearson_r([1, 2, 3], [5, 5, 5])


def test_result_is_rounded_to_4dp():
    r = pearson_r([1, 2, 3, 4, 5], [2, 4, 5, 4, 5])
    assert round(r, 4) == r
    assert r == 0.7746


def test_near_zero_correlation():
    r = pearson_r([1, 2, 3, 4], [3, 1, 1, 3])
    assert r == 0.0


def test_too_few_points():
    with pytest.raises(ValueError):
        pearson_r([1], [2])
