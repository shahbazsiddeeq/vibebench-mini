import pytest

from src.solution import min_max_normalize


def test_worked_example_default_range():
    assert min_max_normalize([10, 20, 30]) == [0.0, 0.5, 1.0]


def test_constant_series():
    assert min_max_normalize([7, 7, 7]) == [0.0, 0.0, 0.0]


def test_single_element():
    assert min_max_normalize([99]) == [0.0]


def test_negatives():
    assert min_max_normalize([-10, 0, 10]) == [0.0, 0.5, 1.0]


def test_empty_raises():
    with pytest.raises(ValueError):
        min_max_normalize([])


def test_constant_series_does_not_divide_by_zero():
    # A naive (x-lo)/(hi-lo) implementation would raise ZeroDivisionError here.
    assert min_max_normalize([4, 4, 4], 0, 1) == [0.0, 0.0, 0.0]
