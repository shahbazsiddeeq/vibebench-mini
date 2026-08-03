"""Least-recently-used cache implementation."""

from collections import OrderedDict
from typing import Hashable


class LRUCache:
    """A fixed-capacity least-recently-used cache."""

    def __init__(self, capacity: int) -> None:
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError("capacity must be an integer")
        if capacity < 1:
            raise ValueError("capacity must be at least 1")

        self._capacity = capacity
        self._cache: OrderedDict[Hashable, int] = OrderedDict()

    def get(self, key: Hashable) -> int:
        """Return the cached value, or -1 if the key is missing."""
        try:
            value = self._cache.pop(key)
        except KeyError:
            return -1

        self._cache[key] = value
        return value

    def put(self, key: Hashable, value: int) -> None:
        """Insert or update a key and mark it as most recently used."""
        if key in self._cache:
            self._cache.pop(key)

        self._cache[key] = value

        if len(self._cache) > self._capacity:
            self._cache.popitem(last=False)
