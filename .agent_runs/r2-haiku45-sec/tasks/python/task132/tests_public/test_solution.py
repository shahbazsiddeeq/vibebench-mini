import threading
import time

import pytest

from src.solution import run_bounded


def test_order_with_variable_work():
    def make(i):
        def fn():
            time.sleep(0.001 * (i % 3))
            return i
        return fn

    fns = [make(i) for i in range(15)]
    assert run_bounded(fns, 4) == list(range(15))


def test_invalid_max_concurrent_raises():
    with pytest.raises(ValueError):
        run_bounded([lambda: 1], 0)


def test_reaches_full_concurrency():
    # With many tasks that all block briefly, the executor should reach its full
    # max_concurrent width. A sequential implementation peaks at 1.
    max_allowed = 5
    lock = threading.Lock()
    state = {"current": 0, "peak": 0}

    def make():
        def fn():
            with lock:
                state["current"] += 1
                state["peak"] = max(state["peak"], state["current"])
            time.sleep(0.02)
            with lock:
                state["current"] -= 1
            return 1
        return fn

    fns = [make() for _ in range(20)]
    results = run_bounded(fns, max_allowed)

    assert results == [1] * 20
    assert state["peak"] >= 2
    assert state["peak"] <= max_allowed
    assert state["current"] == 0
