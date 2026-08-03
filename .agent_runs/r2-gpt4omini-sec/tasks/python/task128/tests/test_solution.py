import threading
import time

import pytest

from src.solution import parallel_map


def test_matches_builtin_map():
    items = list(range(50))
    fn = lambda x: x * x
    assert parallel_map(fn, items) == list(map(fn, items))


def test_order_preserved_with_variable_work():
    # Items sleep for varying durations; result order must still match input.
    def fn(x):
        time.sleep(0.001 * (x % 3))
        return x + 100

    items = list(range(20))
    assert parallel_map(fn, items, workers=4) == [x + 100 for x in items]


def test_single_worker():
    items = [1, 2, 3, 4]
    assert parallel_map(lambda x: x * 2, items, workers=1) == [2, 4, 6, 8]


def test_empty_list():
    assert parallel_map(lambda x: x, []) == []


def test_invalid_workers_raises():
    with pytest.raises(ValueError):
        parallel_map(lambda x: x, [1, 2], workers=0)


def test_actually_runs_concurrently():
    # Probe observed concurrency: with multiple workers and items that block,
    # more than one item must be in flight at once. A sequential (no-thread)
    # implementation has a peak concurrency of exactly 1 and fails here.
    lock = threading.Lock()
    state = {"current": 0, "peak": 0}

    def fn(x):
        with lock:
            state["current"] += 1
            state["peak"] = max(state["peak"], state["current"])
        time.sleep(0.02)
        with lock:
            state["current"] -= 1
        return x

    workers = 4
    result = parallel_map(fn, list(range(8)), workers=workers)
    assert result == list(range(8))
    assert state["peak"] >= 2
    assert state["peak"] <= workers
    assert state["current"] == 0
