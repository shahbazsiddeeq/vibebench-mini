import time


class TTLCache:
    def __init__(self, ttl_seconds, max_size):
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
        self.cache = {}  # key -> (value, timestamp)
        self.access_order = []  # list of keys in insertion order
    
    def get(self, key):
        if key not in self.cache:
            return None
        
        value, timestamp = self.cache[key]
        
        # Check if expired
        if time.time() - timestamp > self.ttl_seconds:
            # Remove expired entry
            del self.cache[key]
            self.access_order.remove(key)
            return None
        
        return value
    
    def set(self, key, value):
        # If max_size is 0 or negative, don't store anything
        if self.max_size <= 0:
            return
        
        current_time = time.time()
        
        # If key already exists, update it
        if key in self.cache:
            self.cache[key] = (value, current_time)
            # Move to end (most recent)
            self.access_order.remove(key)
            self.access_order.append(key)
            return
        
        # If cache is full, make room
        if len(self.cache) >= self.max_size:
            self._evict()
        
        # Add new entry
        self.cache[key] = (value, current_time)
        self.access_order.append(key)
    
    def _evict(self):
        # First, try to remove expired entries
        current_time = time.time()
        expired_keys = []
        
        for key in self.access_order:
            if key in self.cache:
                value, timestamp = self.cache[key]
                if current_time - timestamp > self.ttl_seconds:
                    expired_keys.append(key)
        
        # Remove expired entries
        for key in expired_keys:
            del self.cache[key]
            self.access_order.remove(key)
        
        # If still full after removing expired entries, evict oldest
        if len(self.cache) >= self.max_size:
            oldest_key = self.access_order[0]
            del self.cache[oldest_key]
            self.access_order.remove(oldest_key)
