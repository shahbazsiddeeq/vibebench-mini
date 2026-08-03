import time
from collections import OrderedDict

class TTLCache:
    def __init__(self, ttl_seconds, max_size):
        if not isinstance(ttl_seconds, (int, float)) or ttl_seconds < 0:
            raise ValueError("ttl_seconds must be a non-negative number")
        if not isinstance(max_size, int):
            raise ValueError("max_size must be an integer")
        
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
        self.cache = OrderedDict()

    def _purge_expired(self):
        current_time = time.time()
        keys_to_delete = [key for key, (value, timestamp) in self.cache.items()
                          if current_time - timestamp > self.ttl_seconds]
        for key in keys_to_delete:
            del self.cache[key]

    def get(self, key):
        self._purge_expired()
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp <= self.ttl_seconds:
                return value
        return None

    def set(self, key, value):
        if self.max_size <= 0:
            return

        self._purge_expired()

        if key in self.cache:
            del self.cache[key]
        elif len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)

        self.cache[key] = (value, time.time())
