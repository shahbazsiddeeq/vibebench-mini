"""
LRU Cache implementation.

A secure, self-contained module implementing a Least Recently Used (LRU)
cache with O(1) average-time get/put operations using collections.OrderedDict.

The implementation validates all inputs, avoids any use of eval/exec,
performs no I/O, and does not expose internal state or raise low-level
exceptions with sensitive information.
"""

from collections import OrderedDict
from typing import Any, Hashable


class LRUCache:
    """
    A Least Recently Used (LRU) cache.

    Parameters
    ----------
    capacity : int
        Maximum number of items the cache can hold. Must be >= 1.

    Raises
    ------
    ValueError
        If capacity is not a positive integer.
    """

    def __init__(self, capacity: int) -> None:
        if not isinstance(capacity, int) or isinstance(capacity, bool):
            raise ValueError("capacity must be an integer")
        if capacity < 1:
            raise ValueError("capacity must be >= 1")

        self._capacity: int = capacity
        self._store: "OrderedDict[Hashable, Any]" = OrderedDict()

    def get(self, key: Hashable) -> int:
        """
        Retrieve the value associated with key, marking it as recently used.

        Parameters
        ----------
        key : Hashable
            The key to look up.

        Returns
        -------
        int
            The stored value if present, otherwise -1.
        """
        try:
            if key not in self._store:
                return -1
            value = self._store.pop(key)
            self._store[key] = value
            return value
        except TypeError:
            # Unhashable key type: treat as missing rather than exposing
            # internal error details.
            return -1

    def put(self, key: Hashable, value: int) -> None:
        """
        Insert or update the value for key, marking it as recently used.
        Evicts the least-recently-used item if capacity is exceeded.

        Parameters
        ----------
        key : Hashable
            The key to insert or update.
        value : int
            The value to associate with the key.

        Raises
        ------
        TypeError
            If key is not hashable.
        """
        if not isinstance(key, Hashable):
            raise TypeError("key must be hashable")

        if key in self._store:
            self._store.pop(key)
        elif len(self._store) >= self._capacity:
            # Evict the least-recently-used entry (first item in order).
            self._store.popitem(last=False)

        self._store[key] = value
