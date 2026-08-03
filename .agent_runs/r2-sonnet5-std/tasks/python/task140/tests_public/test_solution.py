import pytest

from src.solution import max_subarray


def test_all_positive_is_whole_array():
    assert max_subarray([1, 2, 3, 4]) == (10, 0, 3)


def test_all_negative_picks_largest_single():
    assert max_subarray([-3, -1, -2]) == (-1, 1, 1)


def test_empty_raises():
    with pytest.raises(ValueError):
        max_subarray([])


def test_tiebreak_smallest_start_with_leading_zeros():
    # Subarrays (0,2),(1,2),(2,2) all sum to 1; smallest start wins.
    assert max_subarray([0, 0, 1]) == (1, 0, 2)


def test_exact_sum_mutation_killer():
    # A greedy solution that never restarts would include the -100.
    res = max_subarray([5, -100, 6, 7])
    assert res == (13, 2, 3)
