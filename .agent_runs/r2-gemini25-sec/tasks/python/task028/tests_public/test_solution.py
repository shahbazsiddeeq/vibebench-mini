import inspect
import random

import pytest
import src.solution as solution_module
from src.solution import quicksort


def test_already_sorted():
    assert quicksort([1, 2, 3, 4]) == [1, 2, 3, 4]


def test_single():
    assert quicksort([42]) == [42]


def test_duplicates():
    assert quicksort([5, 5, 5]) == [5, 5, 5]


@pytest.mark.parametrize(
    "lst,expected",
    [
        ([2, -1, 0, 3], [-1, 0, 2, 3]),
        ([10], [10]),
    ],
)
def test_parametrized(lst, expected):
    assert quicksort(lst) == expected


def test_builtin_sorted_unavailable(monkeypatch):
    def _banned(*args, **kwargs):
        raise AssertionError("built-in sort is not allowed")

    monkeypatch.setattr(solution_module, "sorted", _banned, raising=False)
    assert quicksort([3, 1, 4, 1, 5, 9, 2, 6]) == [1, 1, 2, 3, 4, 5, 6, 9]
