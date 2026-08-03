import pytest
from src.solution import two_sum


def test_basic():
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)


def test_negative_numbers():
    assert two_sum([-3, 0, 3, 5], 0) == (0, 2)


def test_target_zero():
    assert two_sum([-1, 0, 1, 2], 0) == (0, 2)


def test_indices_ordered():
    i, j = two_sum([4, 1, 5, 2], 6)
    assert i < j


def test_multiple_pairs_smallest_j():
    # Valid pairs: (0,4)=10+50 and (1,3)=20+40. Smallest second index is 3.
    assert two_sum([10, 20, 30, 40, 50], 60) == (1, 3)


@pytest.mark.parametrize(
    "nums,target,expected",
    [
        ([1, 5, 3, 2], 7, (1, 3)),  # 5+2=7
        ([0, 4, 3, 0], 0, (0, 3)),
    ],
)
def test_parametrized(nums, target, expected):
    assert two_sum(nums, target) == expected
