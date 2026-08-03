import pytest

from src.solution import majority_element


def test_single_element():
    assert majority_element([5]) == 5


def test_simple_three():
    assert majority_element([3, 3, 4]) == 3


def test_exactly_half_is_not_majority():
    # 2 appears 2 of 4 times -> not strictly more than half.
    with pytest.raises(ValueError):
        majority_element([1, 2, 1, 2])


def test_empty_raises():
    with pytest.raises(ValueError):
        majority_element([])


def test_majority_at_boundary():
    # 5 of 9 -> strict majority.
    assert majority_element([7, 7, 7, 7, 7, 1, 2, 3, 4]) == 7
