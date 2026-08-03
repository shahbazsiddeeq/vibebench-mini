class LRUCache:
    def __init__(self, capacity):
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")
        self.capacity = capacity
        self.cache = {}
        self.order = []  # Track access order, most recent at the end
    
    def get(self, key):
        if key not in self.cache:
            return -1
        
        # Update recency - move to end
        self.order.remove(key)
        self.order.append(key)
        
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            # Update existing key
            self.cache[key] = value
            # Update recency - move to end
            self.order.remove(key)
            self.order.append(key)
        else:
            # New key
            if len(self.cache) >= self.capacity:
                # Evict least recently used (first in order list)
                lru_key = self.order.pop(0)
                del self.cache[lru_key]
            
            self.cache[key] = value
            self.order.append(key)
