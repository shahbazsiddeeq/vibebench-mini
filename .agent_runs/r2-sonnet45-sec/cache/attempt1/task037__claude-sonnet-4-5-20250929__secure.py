from collections import OrderedDict


class LRUCache:
    """
    LRU (Least Recently Used) Cache implementation.
    
    Maintains a cache with a fixed capacity. When the cache is full and a new
    item needs to be added, the least recently used item is evicted.
    """
    
    def __init__(self, capacity: int):
        """
        Initialize the LRU Cache with the given capacity.
        
        Args:
            capacity: Maximum number of items the cache can hold
            
        Raises:
            ValueError: If capacity is less than 1
        """
        if not isinstance(capacity, int) or capacity < 1:
            raise ValueError("Capacity must be a positive integer")
        
        self._capacity = capacity
        self._cache = OrderedDict()
    
    def get(self, key: int) -> int:
        """
        Get the value associated with the key.
        
        Args:
            key: The key to look up
            
        Returns:
            The value associated with the key, or -1 if the key doesn't exist
        """
        if key not in self._cache:
            return -1
        
        # Move to end to mark as recently used
        self._cache.move_to_end(key)
        return self._cache[key]
    
    def put(self, key: int, value: int) -> None:
        """
        Put a key-value pair into the cache.
        
        If the key already exists, update its value and mark it as recently used.
        If the cache is at capacity and the key is new, evict the least recently
        used item before adding the new one.
        
        Args:
            key: The key to store
            value: The value to associate with the key
        """
        if key in self._cache:
            # Update existing key and move to end
            self._cache[key] = value
            self._cache.move_to_end(key)
        else:
            # Add new key
            if len(self._cache) >= self._capacity:
                # Remove least recently used (first item)
                self._cache.popitem(last=False)
            self._cache[key] = value
