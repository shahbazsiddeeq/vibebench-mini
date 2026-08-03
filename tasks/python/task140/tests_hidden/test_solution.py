import pytest

from src.solution import max_subarray


def test_classic_example():
    assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == (6, 3, 6)


def test_single_element():
    assert max_subarray([7]) == (7, 0, 0)


def test_all_negative_first_element():
    assert max_subarray([-1, -5, -9]) == (-1, 0, 0)


def test_tiebreak_shortest_smallest_end_with_trailing_zeros():
    # Subarrays (0,0),(0,1),(0,2) all sum to 1; smallest end wins.
    assert max_subarray([1, 0, 0]) == (1, 0, 0)


def test_negative_then_positive_block():
    # Best is the [4,-1,2] block (sum 5) starting at index 2.
    assert max_subarray([-10, -10, 4, -1, 2]) == (5, 2, 4)


def test_zeros_only():
    assert max_subarray([0, 0, 0]) == (0, 0, 0)
