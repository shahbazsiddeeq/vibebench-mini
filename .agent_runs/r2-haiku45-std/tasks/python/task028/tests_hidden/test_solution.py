import inspect
import random

import pytest
import src.solution as solution_module
from src.solution import quicksort


def test_basic():
    assert quicksort([3, 1, 4, 1, 5, 9, 2, 6]) == [1, 1, 2, 3, 4, 5, 6, 9]


def test_reverse_sorted():
    assert quicksort([4, 3, 2, 1]) == [1, 2, 3, 4]


def test_empty():
    assert quicksort([]) == []


def test_returns_new_list():
    original = [3, 1, 2]
    result = quicksort(original)
    assert original == [3, 1, 2]
    assert result == [1, 2, 3]


def test_does_not_use_builtin_sort():
    src = inspect.getsource(solution_module)
    assert "sorted(" not in src, "must not use the built-in sorted()"
    assert ".sort(" not in src, "must not use list.sort()"


def test_randomized_large_input():
    rng = random.Random(1234)
    for _ in range(20):
        data = [rng.randint(-1000, 1000) for _ in range(500)]
        assert quicksort(data) == sorted(data)
