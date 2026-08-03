import threading
import time

import pytest

from src.solution import run_bounded


def test_results_in_order():
    fns = [lambda i=i: i * i for i in range(10)]
    assert run_bounded(fns, 3) == [i * i for i in range(10)]


def test_empty_returns_empty():
    assert run_bounded([], 4) == []


def test_max_concurrency_respected():
    max_allowed = 3
    lock = threading.Lock()
    state = {"current": 0, "peak": 0}

    def make():
        def fn():
            with lock:
                state["current"] += 1
                state["peak"] = max(state["peak"], state["current"])
            time.sleep(0.005)
            with lock:
                state["current"] -= 1
            return "ok"
        return fn

    fns = [make() for _ in range(30)]
    results = run_bounded(fns, max_allowed)

    assert results == ["ok"] * 30
    # Upper bound: never more than max_concurrent at once.
    assert state["peak"] <= max_allowed
    # Lower bound: work must actually run concurrently. A sequential (no-thread)
    # implementation has a peak of exactly 1 and fails here.
    assert state["peak"] >= 2
    assert state["current"] == 0
