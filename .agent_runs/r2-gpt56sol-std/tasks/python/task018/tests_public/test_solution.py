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


def test_found_first():
    assert binary_search([1, 3, 5, 7, 9], 1) == 0


def test_not_found():
    assert binary_search([1, 3, 5, 7, 9], 4) == -1


def test_single_found():
    assert binary_search([42], 42) == 0


def test_even_length():
    arr = [2, 4, 6, 8]
    assert binary_search(arr, 2) == 0
    assert binary_search(arr, 8) == 3
    assert binary_search(arr, 6) == 2
    assert binary_search(arr, 5) == -1
    assert binary_search(arr, 9) == -1


def test_large_input():
    arr = list(range(0, 2_000_000, 2))  # even numbers 0..1999998
    assert binary_search(arr, 1_500_000) == 750_000
    assert binary_search(arr, 0) == 0
    assert binary_search(arr, 1_999_998) == len(arr) - 1
    assert binary_search(arr, 1_500_001) == -1  # odd -> absent


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
