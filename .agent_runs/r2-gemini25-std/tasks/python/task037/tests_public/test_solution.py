import pytest
from src.solution import LRUCache


def test_missing_returns_minus_one():
    c = LRUCache(1)
    assert c.get(99) == -1


def test_access_updates_recency():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.get(1)
    c.put(3, 3)
    assert c.get(1) == 1
    assert c.get(2) == -1


def test_update_existing():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(1, 100)
    assert c.get(1) == 100


def test_negative_capacity_raises():
    with pytest.raises(ValueError):
        LRUCache(-1)
