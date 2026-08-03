import time
from collections import OrderedDict


class TTLCache:
    """A size-bounded cache whose entries expire after ttl_seconds.

    - get(key) returns the value, or None if the key is missing or expired.
    - set(key, value) inserts/updates the key.
    - Expired entries are reclaimed lazily (on get) and are also purged before
      a capacity-based eviction, so a stale entry is dropped before any live
      entry is evicted.
    - max_size <= 0 means the cache holds nothing (set is a no-op).
    """

    def __init__(self, ttl_seconds: float, max_size: int):
        self._ttl = ttl_seconds
        self._max_size = max_size
        self._store: OrderedDict = OrderedDict()

    def _purge_expired(self, now: float) -> None:
        expired = [k for k, (_, exp) in self._store.items() if now > exp]
        for k in expired:
            del self._store[k]

    def get(self, key):
        if key not in self._store:
            return None
        value, expires_at = self._store[key]
        if time.monotonic() > expires_at:
            del self._store[key]
            return None
        return value

    def set(self, key, value):
        now = time.monotonic()
        if self._max_size <= 0:
            return
        if key in self._store:
            del self._store[key]
        # Reclaim expired entries first so we never evict a live entry while a
        # stale one is still occupying space.
        self._purge_expired(now)
        while len(self._store) >= self._max_size:
            self._store.popitem(last=False)
        self._store[key] = (value, now + self._ttl)
