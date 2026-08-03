import time
from collections import OrderedDict


class TTLCache:
    def __init__(self, ttl_seconds, max_size):
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
        self.cache = OrderedDict()  # Maps key -> (value, timestamp)
    
    def get(self, key):
        """Returns the value if key exists and hasn't expired, otherwise None."""
        if key not in self.cache:
            return None
        
        value, timestamp = self.cache[key]
        current_time = time.time()
        
        # Check if the entry has expired
        if current_time - timestamp > self.ttl_seconds:
            del self.cache[key]
            return None
        
        return value
    
    def set(self, key, value):
        """Stores/updates a key-value pair."""
        if self.max_size <= 0:
            return
        
        current_time = time.time()
        
        # If key already exists, remove it first (we'll re-add it at the end)
        if key in self.cache:
            del self.cache[key]
        
        # Remove expired entries
        expired_keys = []
        for k, (v, timestamp) in self.cache.items():
            if current_time - timestamp > self.ttl_seconds:
                expired_keys.append(k)
        
        for k in expired_keys:
            del self.cache[k]
        
        # If cache is still full, evict the oldest remaining entry
        while len(self.cache) >= self.max_size:
            # Remove the oldest entry (first item in OrderedDict)
            self.cache.popitem(last=False)
        
        # Add the new entry
        self.cache[key] = (value, current_time)
