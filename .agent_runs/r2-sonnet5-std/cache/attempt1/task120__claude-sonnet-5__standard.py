import time
from collections import OrderedDict


class TTLCache:
    def __init__(self, ttl_seconds, max_size):
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
        self.store = OrderedDict()  # key -> (value, expire_at)

    def _is_expired(self, expire_at, now=None):
        if now is None:
            now = time.time()
        return expire_at <= now

    def _purge_expired(self):
        now = time.time()
        expired_keys = [k for k, (v, exp) in self.store.items() if self._is_expired(exp, now)]
        for k in expired_keys:
            del self.store[k]

    def get(self, key):
        if key not in self.store:
            return None
        value, expire_at = self.store[key]
        if self._is_expired(expire_at):
            del self.store[key]
            return None
        return value

    def set(self, key, value):
        if self.max_size <= 0:
            return

        now = time.time()
        expire_at = now + self.ttl_seconds

        if key in self.store:
            del self.store[key]
            self.store[key] = (value, expire_at)
            return

        if len(self.store) >= self.max_size:
            self._purge_expired()

        if len(self.store) >= self.max_size:
            oldest_key = next(iter(self.store))
            del self.store[oldest_key]

        self.store[key] = (value, expire_at)
