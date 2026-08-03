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


def test_present_multiple():
    assert count_occurrences([1, 2, 2, 2, 3], 2) == 3


def test_not_present():
    assert count_occurrences([1, 2, 3], 5) == 0


def test_all_same():
    assert count_occurrences([7, 7, 7, 7], 7) == 4


def test_below_minimum():
    assert count_occurrences([2, 4, 6, 8], 1) == 0


def test_uses_binary_search():
    n = 200_000
    data = [i // 2 for i in range(n)]  # each value 0..n/2-1 appears twice
    seq = _CountingSeq(data)
    assert count_occurrences(seq, 12345) == 2
    # O(log n) access budget; a linear scan would need ~n accesses.
    assert seq.accesses <= 80, f"too many accesses: {seq.accesses}"
