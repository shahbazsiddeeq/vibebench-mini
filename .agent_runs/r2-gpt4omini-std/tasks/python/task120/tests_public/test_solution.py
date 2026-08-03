import time

from src.solution import TTLCache


def test_missing_returns_none():
    c = TTLCache(60, 10)
    assert c.get("missing") is None


def test_max_size_evicts_oldest():
    c = TTLCache(60, 2)
    c.set("a", 1)
    c.set("b", 2)
    c.set("c", 3)
    assert c.get("a") is None
    assert c.get("b") == 2
    assert c.get("c") == 3


def test_max_size_zero_holds_nothing():
    c = TTLCache(60, 0)
    c.set("x", 1)  # must not raise
    assert c.get("x") is None


def test_expired_entries_reclaimed_before_evicting_live():
    # Fill the cache, let those entries expire, then insert fresh live entries.
    # The expired entries must be reclaimed so the live ones survive.
    c = TTLCache(0.05, 2)
    c.set("a", 1)
    c.set("b", 2)
    time.sleep(0.08)  # a and b now expired
    c.set("c", 3)
    c.set("d", 4)
    assert c.get("a") is None
    assert c.get("b") is None
    assert c.get("c") == 3
    assert c.get("d") == 4
