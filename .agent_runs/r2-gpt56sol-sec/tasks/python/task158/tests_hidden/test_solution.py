import pytest

from src.solution import linear_regression


def test_worked_example():
    assert linear_regression([1, 2, 3, 4], [6, 5, 7, 10]) == (1.4, 3.5)


def test_perfect_line_with_intercept():
    assert linear_regression([0, 1, 2], [1, 3, 5]) == (2.0, 1.0)


def test_returns_floats():
    slope, intercept = linear_regression([1, 2, 3], [1, 2, 3])
    assert isinstance(slope, float) and isinstance(intercept, float)


def test_length_mismatch_raises():
    with pytest.raises(ValueError):
        linear_regression([1, 2, 3], [1, 2])


def test_constant_x_raises():
    with pytest.raises(ValueError):
        linear_regression([2, 2, 2], [1, 2, 3])
