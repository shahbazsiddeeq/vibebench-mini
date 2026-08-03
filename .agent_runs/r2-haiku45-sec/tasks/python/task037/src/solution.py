from collections import OrderedDict


class LRUCache:
    """
    Least Recently Used (LRU) Cache implementation.
    
    Maintains a cache with a fixed capacity. When the cache is full and a new
    item is added, the least recently used item is evicted.
    """
    
    def __init__(self, capacity: int) -> None:
        """
        Initialize the LRU cache.
        
        Args:
            capacity: Maximum number of items the cache can hold.
            
        Raises:
            ValueError: If capacity is less than 1.
        """
        if not isinstance(capacity, int) or capacity < 1:
            raise ValueError("Capacity must be an integer >= 1")
        
        self.capacity = capacity
        self.cache: OrderedDict = OrderedDict()
    
    def get(self, key: int) -> int:
        """
        Retrieve a value from the cache.
        
        Accessing an item marks it as recently used.
        
        Args:
            key: The key to look up.
            
        Returns:
            The value associated with the key, or -1 if not found.
        """
        if not isinstance(key, int):
            raise TypeError("Key must be an integer")
        
        if key not in self.cache:
            return -1
        
        # Move to end to mark as recently used
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key: int, value: int) -> None:
        """
        Insert or update a key-value pair in the cache.
        
        If the key already exists, its value is updated and it's marked as
        recently used. If the cache is at capacity, the least recently used
        item is evicted before insertion.
        
        Args:
            key: The key to insert or update.
            value: The value to associate with the key.
            
        Raises:
            TypeError: If key or value is not an integer.
        """
        if not isinstance(key, int):
            raise TypeError("Key must be an integer")
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        
        if key in self.cache:
            # Update existing key and move to end (most recently used)
            self.cache[key] = value
            self.cache.move_to_end(key)
        else:
            # Add new key
            if len(self.cache) >= self.capacity:
                # Evict least recently used (first item)
                self.cache.popitem(last=False)
            
            self.cache[key] = value
