import pytest

from src.solution import min_max_normalize


def test_worked_example_custom_range():
    assert min_max_normalize([10, 20, 30], 0, 100) == [0.0, 50.0, 100.0]


def test_constant_series_custom_new_min():
    assert min_max_normalize([5, 5], -3, 3) == [-3.0, -3.0]


def test_returns_floats():
    out = min_max_normalize([1, 2, 3])
    assert all(isinstance(v, float) for v in out)


def test_input_not_mutated():
    data = [10, 20, 30]
    min_max_normalize(data)
    assert data == [10, 20, 30]


def test_rounding_enforced():
    # 1/3 of the span produces a repeating decimal that must round to 6 places.
    assert min_max_normalize([0, 1, 3])[1] == 0.333333
