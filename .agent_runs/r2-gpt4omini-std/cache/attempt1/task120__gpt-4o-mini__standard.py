import time
from collections import OrderedDict

class TTLCache:
    def __init__(self, ttl_seconds: float, max_size: int):
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
        self.cache = OrderedDict()

    def _cleanup(self):
        current_time = time.time()
        # Remove expired entries
        for key in list(self.cache.keys()):
            if current_time - self.cache[key][1] > self.ttl_seconds:
                del self.cache[key]
        
        # If max_size is reached, evict the oldest entry
        if self.max_size > 0 and len(self.cache) > self.max_size:
            self.cache.popitem(last=False)

    def get(self, key):
        self._cleanup()
        if key in self.cache:
            return self.cache[key][0]
        return None

    def set(self, key, value):
        if self.max_size <= 0:
            return
        self._cleanup()
        self.cache[key] = (value, time.time())
        self._cleanup()
