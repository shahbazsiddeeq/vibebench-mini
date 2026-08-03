import threading
import time

import pytest

from src.solution import parallel_map


def test_matches_builtin_map():
    items = list(range(50))
    fn = lambda x: x * x
    assert parallel_map(fn, items) == list(map(fn, items))


def test_single_worker():
    items = [1, 2, 3, 4]
    assert parallel_map(lambda x: x * 2, items, workers=1) == [2, 4, 6, 8]


def test_invalid_workers_raises():
    with pytest.raises(ValueError):
        parallel_map(lambda x: x, [1, 2], workers=0)
