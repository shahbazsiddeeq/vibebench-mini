import time

from src.solution import TTLCache


def test_get_set():
    c = TTLCache(60, 10)
    c.set("x", 1)
    assert c.get("x") == 1


def test_expiry():
    c = TTLCache(0.05, 10)
    c.set("x", 42)
    time.sleep(0.1)
    assert c.get("x") is None


def test_overwrite():
    c = TTLCache(60, 10)
    c.set("x", 1)
    c.set("x", 99)
    assert c.get("x") == 99


def test_negative_max_size_holds_nothing():
    c = TTLCache(60, -5)
    c.set("a", 1)
    c.set("b", 2)
    assert c.get("a") is None
    assert c.get("b") is None
