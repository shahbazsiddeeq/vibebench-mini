import pytest

from src.solution import majority_element


def test_basic_majority():
    assert majority_element([2, 2, 1, 1, 1, 2, 2]) == 2


def test_all_same():
    assert majority_element([9, 9, 9]) == 9


def test_no_majority_raises():
    with pytest.raises(ValueError):
        majority_element([1, 2, 3])


def test_verification_kills_false_positive():
    # Boyer-Moore candidate here is 4 (count survives), but 4 is not a majority.
    with pytest.raises(ValueError):
        majority_element([1, 2, 3, 4, 4])


def test_negatives_majority():
    assert majority_element([-1, -1, -1, 2, 3]) == -1


def test_interleaved_majority():
    assert majority_element([1, 2, 1, 2, 1]) == 1
