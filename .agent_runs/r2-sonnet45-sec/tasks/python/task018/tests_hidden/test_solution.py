import pytest
from src.solution import binary_search






















class _CountingList(list):
    """List that counts element accesses to prove logarithmic behaviour."""

    def __init__(self, *args):
        super().__init__(*args)
        self.accesses = 0

    def __getitem__(self, idx):
        self.accesses += 1
        return super().__getitem__(idx)


def test_found_middle():
    assert binary_search([1, 3, 5, 7, 9], 5) == 2


def test_found_last():
    assert binary_search([1, 3, 5, 7, 9], 9) == 4


def test_empty():
    assert binary_search([], 1) == -1


def test_single_not_found():
    assert binary_search([42], 1) == -1


def test_duplicates_returns_valid_index():
    arr = [1, 2, 2, 2, 2, 3]
    idx = binary_search(arr, 2)
    assert idx != -1
    assert arr[idx] == 2


def test_is_logarithmic():
    n = 100_000
    arr = _CountingList(range(n))
    # target absent, forcing a full search path
    assert binary_search(arr, -1) == -1
    # A linear scan would touch ~n elements; O(log n) stays tiny.
    assert arr.accesses <= 40, f"too many accesses: {arr.accesses}"
