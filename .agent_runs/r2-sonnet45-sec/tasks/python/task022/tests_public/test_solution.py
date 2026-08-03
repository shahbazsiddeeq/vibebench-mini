import pytest
from src.solution import two_sum


def test_not_adjacent():
    assert two_sum([1, 3, 5, 7], 8) == (1, 2)  # 3+5=8


def test_no_solution_raises():
    with pytest.raises(ValueError):
        two_sum([1, 2, 3], 10)


def test_duplicates():
    assert two_sum([3, 3, 4], 6) == (0, 1)


def test_prefers_smallest_second_index():
    # A brute force that returns the smallest FIRST index would give (0, 3)
    # (1+7=8); the required answer is the smallest second index: (1, 2).
    assert two_sum([1, 3, 5, 7], 8) == (1, 2)


def test_repeated_complement_uses_closest_i():
    # value 3 appears at indices 0 and 1; the partner for index 2 is the
    # closest preceding one (index 1).
    assert two_sum([3, 3, 3], 6) == (0, 1)
