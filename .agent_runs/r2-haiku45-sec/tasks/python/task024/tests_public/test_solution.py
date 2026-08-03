import pytest
from src.solution import count_occurrences


















class _CountingSeq:
    """Sorted sequence that records every element access.

    A linear scan (or ``arr.count(target)``, which this object does not even
    provide) would touch every element; binary search touches O(log n).
    """

    def __init__(self, data):
        self._data = data
        self.accesses = 0

    def __len__(self):
        return len(self._data)

    def __getitem__(self, idx):
        self.accesses += 1
        return self._data[idx]


def test_present_once():
    assert count_occurrences([1, 2, 3, 4], 3) == 1


def test_empty():
    assert count_occurrences([], 1) == 0


def test_at_boundaries():
    assert count_occurrences([1, 1, 2, 3, 3], 1) == 2
    assert count_occurrences([1, 1, 2, 3, 3], 3) == 2


def test_above_maximum():
    assert count_occurrences([2, 4, 6, 8], 99) == 0


@pytest.mark.parametrize(
    "arr,target,expected",
    [
        ([1], 1, 1),
        ([1], 2, 0),
        ([1, 2, 3, 3, 3, 4], 3, 3),
    ],
)
def test_parametrized(arr, target, expected):
    assert count_occurrences(arr, target) == expected
