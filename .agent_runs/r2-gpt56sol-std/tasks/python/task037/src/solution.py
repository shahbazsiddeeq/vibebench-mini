from collections import OrderedDict
from typing import Hashable


class LRUCache:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.capacity = capacity
        self._cache: OrderedDict[Hashable, int] = OrderedDict()

    def get(self, key: Hashable) -> int:
        if key not in self._cache:
            return -1
        self._cache.move_to_end(key)
        return self._cache[key]

    def put(self, key: Hashable, value: int) -> None:
        if key in self._cache:
            self._cache[key] = value
            self._cache.move_to_end(key)
            return

        if len(self._cache) >= self.capacity:
            self._cache.popitem(last=False)

        self._cache[key] = value
