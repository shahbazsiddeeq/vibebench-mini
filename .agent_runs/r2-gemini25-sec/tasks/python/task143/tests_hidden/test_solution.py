import random

import pytest

from src.solution import kth_largest


def test_basic_second_largest():
    assert kth_largest([3, 2, 1, 5, 6, 4], 2) == 5


def test_smallest_is_last():
    assert kth_largest([3, 2, 1, 5, 6, 4], 6) == 1


def test_duplicates_counted_by_position():
    assert kth_largest([3, 3, 3], 2) == 3


def test_negatives():
    assert kth_largest([-1, -5, -3, -2], 1) == -1
    assert kth_largest([-1, -5, -3, -2], 4) == -5


def test_empty_raises():
    with pytest.raises(ValueError):
        kth_largest([], 1)


def test_k_zero_raises():
    with pytest.raises(ValueError):
        kth_largest([1, 2, 3], 0)


def test_does_not_mutate_input():
    data = [3, 1, 2]
    _ = kth_largest(data, 2)
    assert data == [3, 1, 2]
