import pytest

from src.solution import weighted_average


def test_returns_float():
    assert isinstance(weighted_average([1, 2], [1, 1]), float)


def test_equal_weights_equals_plain_mean():
    assert weighted_average([2, 4, 6], [1, 1, 1]) == 4.0


def test_empty_raises():
    with pytest.raises(ValueError):
        weighted_average([], [])


def test_zero_total_weight_raises():
    with pytest.raises(ValueError):
        weighted_average([1, 2], [1, -1])


def test_rounding_to_six_places():
    # 1/3 weighting scenario forcing a repeating decimal.
    assert weighted_average([0, 1, 0], [1, 1, 1]) == 0.333333
