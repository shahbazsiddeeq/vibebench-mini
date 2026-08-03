import pytest
from src.solution import binary_search


def test_found_middle():
    assert binary_search([1, 3, 5, 7, 9], 5) == 2


def test_found_first():
    assert binary_search([1, 3, 5, 7, 9], 1) == 0


def test_found_last():
    assert binary_search([1, 3, 5, 7, 9], 9) == 4


def test_not_found():
    assert binary_search([1, 3, 5, 7, 9], 4) == -1


def test_empty():
    assert binary_search([], 1) == -1


def test_single_found():
    assert binary_search([42], 42) == 0


def test_single_not_found():
    assert binary_search([42], 1) == -1


def test_even_length():
    arr = [2, 4, 6, 8]
    assert binary_search(arr, 2) == 0
    assert binary_search(arr, 8) == 3
    assert binary_search(arr, 6) == 2
    assert binary_search(arr, 5) == -1
    assert binary_search(arr, 9) == -1


def test_duplicates_returns_valid_index():
    arr = [1, 2, 2, 2, 2, 3]
    idx = binary_search(arr, 2)
    assert idx != -1
    assert arr[idx] == 2


def test_large_input():
    arr = list(range(0, 2_000_000, 2))  # even numbers 0..1999998
    assert binary_search(arr, 1_500_000) == 750_000
    assert binary_search(arr, 0) == 0
    assert binary_search(arr, 1_999_998) == len(arr) - 1
    assert binary_search(arr, 1_500_001) == -1  # odd -> absent


class _CountingList(list):
    """List that counts element accesses to prove logarithmic behaviour."""

    def __init__(self, *args):
        super().__init__(*args)
        self.accesses = 0

    def __getitem__(self, idx):
        self.accesses += 1
        return super().__getitem__(idx)


def test_is_logarithmic():
    n = 100_000
    arr = _CountingList(range(n))
    # target absent, forcing a full search path
    assert binary_search(arr, -1) == -1
    # A linear scan would touch ~n elements; O(log n) stays tiny.
    assert arr.accesses <= 40, f"too many accesses: {arr.accesses}"


@pytest.mark.parametrize(
    "arr,target,expected",
    [
        ([2, 4, 6, 8, 10], 6, 2),
        ([2, 4, 6, 8, 10], 10, 4),
        ([2, 4, 6, 8, 10], 1, -1),
        ([1, 2, 3, 4, 5, 6], 4, 3),
        ([1, 2, 3, 4, 5, 6], 7, -1),
    ],
)
def test_parametrized(arr, target, expected):
    assert binary_search(arr, target) == expected
