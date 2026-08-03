import pytest
from src.solution import LRUCache


def test_basic_put_get():
    c = LRUCache(2)
    c.put(1, 1)
    assert c.get(1) == 1


def test_missing_returns_minus_one():
    c = LRUCache(1)
    assert c.get(99) == -1


def test_eviction():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(3, 3)
    assert c.get(1) == -1
    assert c.get(3) == 3


def test_access_updates_recency():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.get(1)
    c.put(3, 3)
    assert c.get(1) == 1
    assert c.get(2) == -1


def test_capacity_one():
    c = LRUCache(1)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == -1
    assert c.get(2) == 2


def test_update_existing():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(1, 100)
    assert c.get(1) == 100


def test_capacity_zero_raises():
    with pytest.raises(ValueError):
        LRUCache(0)


def test_negative_capacity_raises():
    with pytest.raises(ValueError):
        LRUCache(-1)


def test_update_existing_bumps_recency():
    # Updating an existing key must mark it as most-recently-used.
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(1, 10)  # 1 becomes most recent; 2 is now least-recently-used
    c.put(3, 3)  # should evict 2, not 1
    assert c.get(2) == -1
    assert c.get(1) == 10
    assert c.get(3) == 3
