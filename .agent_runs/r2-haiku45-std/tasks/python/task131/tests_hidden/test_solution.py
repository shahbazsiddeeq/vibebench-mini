import sys
import threading
import time

import pytest

from src.solution import Once


def test_returns_first_value():
    o = Once()
    assert o.do(lambda: 5) == 5


def test_fn_runs_only_once_single_thread():
    o = Once()
    calls = []
    o.do(lambda: calls.append(1))
    o.do(lambda: calls.append(1))
    o.do(lambda: calls.append(1))
    assert len(calls) == 1


def test_exception_allows_retry():
    o = Once()
    attempts = []

    def failing():
        attempts.append(1)
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        o.do(failing)
    # A raising fn is not recorded as done, so it runs again next time.
    with pytest.raises(RuntimeError):
        o.do(failing)
    assert len(attempts) == 2

    # Once it finally succeeds, that value is cached permanently.
    assert o.do(lambda: "ok") == "ok"
    assert o.do(lambda: "different") == "ok"
