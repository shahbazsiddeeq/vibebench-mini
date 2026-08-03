import pytest

from src.solution import linear_regression


def test_worked_example():
    assert linear_regression([1, 2, 3, 4], [6, 5, 7, 10]) == (1.4, 3.5)


def test_perfect_line_through_origin():
    assert linear_regression([1, 2, 3], [2, 4, 6]) == (2.0, 0.0)


def test_perfect_line_with_intercept():
    assert linear_regression([0, 1, 2], [1, 3, 5]) == (2.0, 1.0)


def test_negative_slope():
    assert linear_regression([1, 2, 3], [3, 2, 1]) == (-1.0, 4.0)


def test_returns_floats():
    slope, intercept = linear_regression([1, 2, 3], [1, 2, 3])
    assert isinstance(slope, float) and isinstance(intercept, float)


def test_two_points():
    assert linear_regression([0, 10], [0, 5]) == (0.5, 0.0)


def test_length_mismatch_raises():
    with pytest.raises(ValueError):
        linear_regression([1, 2, 3], [1, 2])


def test_too_few_points_raises():
    with pytest.raises(ValueError):
        linear_regression([1], [1])


def test_constant_x_raises():
    with pytest.raises(ValueError):
        linear_regression([2, 2, 2], [1, 2, 3])


def test_rounding_enforced():
    # slope = 1/3 forces a repeating decimal that must round to 6 places.
    slope, intercept = linear_regression([0, 1, 2], [0, 0, 1])
    assert slope == 0.5
    # A case that genuinely needs rounding:
    slope2, _ = linear_regression([0, 1, 2], [0, 1, 1])
    assert slope2 == 0.5
    slope3, intercept3 = linear_regression([1, 2, 3], [1, 2, 2])
    assert slope3 == 0.5
    assert intercept3 == 0.666667
