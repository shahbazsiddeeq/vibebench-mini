import time
from collections import OrderedDict


class TTLCache:
    """A time-to-live cache that expires entries and evicts oldest when full."""
    
    def __init__(self, ttl_seconds, max_size):
        """
        Initialize a TTL cache.
        
        Args:
            ttl_seconds: Time in seconds before entries expire
            max_size: Maximum number of entries; <= 0 means cache holds nothing
        """
        if not isinstance(ttl_seconds, (int, float)) or ttl_seconds < 0:
            raise ValueError("ttl_seconds must be non-negative")
        if not isinstance(max_size, int):
            raise ValueError("max_size must be an integer")
        
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
        # OrderedDict maintains insertion order for FIFO eviction
        self.cache = OrderedDict()
        # Store expiration time for each key
        self.expiry_times = {}
    
    def get(self, key):
        """
        Retrieve a value from the cache.
        
        Args:
            key: The key to look up
            
        Returns:
            The value if the key exists and hasn't expired, None otherwise
        """
        if not isinstance(key, str):
            raise ValueError("key must be a string")
        
        if key not in self.cache:
            return None
        
        # Check if the entry has expired
        if time.time() >= self.expiry_times[key]:
            # Entry has expired, remove it
            del self.cache[key]
            del self.expiry_times[key]
            return None
        
        return self.cache[key]
    
    def set(self, key, value):
        """
        Store or update a key-value pair in the cache.
        
        Args:
            key: The key to store
            value: The value to store
        """
        if not isinstance(key, str):
            raise ValueError("key must be a string")
        
        # If max_size <= 0, cache holds nothing
        if self.max_size <= 0:
            return
        
        # If key already exists, update it and move to end (most recent)
        if key in self.cache:
            del self.cache[key]
            del self.expiry_times[key]
        
        # Remove expired entries first
        current_time = time.time()
        expired_keys = [k for k in self.cache if current_time >= self.expiry_times[k]]
        for k in expired_keys:
            del self.cache[k]
            del self.expiry_times[k]
        
        # If still at capacity, evict the oldest (first) entry
        if len(self.cache) >= self.max_size:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
            del self.expiry_times[oldest_key]
        
        # Add the new entry
        self.cache[key] = value
        self.expiry_times[key] = current_time + self.ttl_seconds
