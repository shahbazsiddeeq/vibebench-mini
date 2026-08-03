# src/solution.py

import time
from collections import OrderedDict

class TTLCache:
    def __init__(self, ttl_seconds: float, max_size: int):
        if not isinstance(ttl_seconds, (int, float)) or ttl_seconds < 0:
            raise ValueError("ttl_seconds must be a non-negative number.")
        if not isinstance(max_size, int) or max_size < 0:
            raise ValueError("max_size must be a non-negative integer.")
        
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
        self.cache = OrderedDict()

    def _clean_expired(self):
        current_time = time.time()
        keys_to_delete = [key for key, (value, timestamp) in self.cache.items() if current_time - timestamp > self.ttl_seconds]
        for key in keys_to_delete:
            del self.cache[key]

    def get(self, key):
        if not isinstance(key, str):
            raise ValueError("Key must be a string.")
        
        self._clean_expired()
        if key in self.cache:
            value, _ = self.cache[key]
            return value
        return None

    def set(self, key, value):
        if not isinstance(key, str):
            raise ValueError("Key must be a string.")
        if self.max_size <= 0:
            return
        
        self._clean_expired()
        
        if key in self.cache:
            self.cache.move_to_end(key)
        
        self.cache[key] = (value, time.time())
        
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)
