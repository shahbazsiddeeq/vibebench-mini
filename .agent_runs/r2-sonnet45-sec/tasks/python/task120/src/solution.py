import time
from collections import OrderedDict


class TTLCache:
    """
    A cache with time-to-live (TTL) expiration and size limit.
    
    Entries expire after ttl_seconds. When the cache is full, expired entries
    are reclaimed first, then the oldest remaining entry is evicted.
    """
    
    def __init__(self, ttl_seconds, max_size):
        """
        Initialize the TTL cache.
        
        Args:
            ttl_seconds: Time in seconds after which entries expire
            max_size: Maximum number of entries (<=0 means cache holds nothing)
        """
        # Validate inputs
        if not isinstance(ttl_seconds, (int, float)):
            raise TypeError("ttl_seconds must be a number")
        if not isinstance(max_size, int):
            raise TypeError("max_size must be an integer")
        if ttl_seconds < 0:
            raise ValueError("ttl_seconds cannot be negative")
        
        self._ttl_seconds = ttl_seconds
        self._max_size = max_size
        # Use OrderedDict to maintain insertion order for LRU eviction
        self._cache = OrderedDict()
        # Store expiration times separately
        self._expiry = {}
    
    def _is_expired(self, key):
        """Check if a key has expired."""
        if key not in self._expiry:
            return True
        return time.time() > self._expiry[key]
    
    def _remove_expired(self):
        """Remove all expired entries from the cache."""
        current_time = time.time()
        expired_keys = [
            key for key, expiry_time in self._expiry.items()
            if current_time > expiry_time
        ]
        for key in expired_keys:
            self._cache.pop(key, None)
            self._expiry.pop(key, None)
    
    def get(self, key):
        """
        Retrieve a value from the cache.
        
        Args:
            key: The key to look up
            
        Returns:
            The value if the key exists and hasn't expired, None otherwise
        """
        # Validate key type (must be hashable)
        try:
            hash(key)
        except TypeError:
            return None
        
        if key not in self._cache:
            return None
        
        if self._is_expired(key):
            # Clean up expired entry
            self._cache.pop(key, None)
            self._expiry.pop(key, None)
            return None
        
        return self._cache[key]
    
    def set(self, key, value):
        """
        Store a key-value pair in the cache.
        
        Args:
            key: The key to store
            value: The value to store
        """
        # If max_size <= 0, cache holds nothing
        if self._max_size <= 0:
            return
        
        # Validate key type (must be hashable)
        try:
            hash(key)
        except TypeError:
            return
        
        # If key already exists, remove it first (will be re-added at end)
        if key in self._cache:
            self._cache.pop(key)
            self._expiry.pop(key, None)
        
        # Remove expired entries first
        self._remove_expired()
        
        # If still at capacity, evict oldest entry
        while len(self._cache) >= self._max_size:
            # Remove oldest entry (first item in OrderedDict)
            oldest_key = next(iter(self._cache))
            self._cache.pop(oldest_key)
            self._expiry.pop(oldest_key, None)
        
        # Add new entry
        self._cache[key] = value
        self._expiry[key] = time.time() + self._ttl_seconds
