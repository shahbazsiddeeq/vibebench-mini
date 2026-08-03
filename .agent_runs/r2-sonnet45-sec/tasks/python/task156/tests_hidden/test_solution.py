import pytest

from src.solution import weighted_average


def test_worked_example():
    assert weighted_average([80, 90, 100], [1, 2, 3]) == 93.333333


def test_single_element():
    assert weighted_average([42], [5]) == 42.0


def test_negatives():
    assert weighted_average([-10, 10], [3, 1]) == -5.0


def test_length_mismatch_raises():
    with pytest.raises(ValueError):
        weighted_average([1, 2, 3], [1, 2])


def test_weighting_actually_applied():
    # Unweighted mean would be 90.0; correct weighted answer is not 90.0.
    assert weighted_average([80, 90, 100], [1, 2, 3]) != 90.0
