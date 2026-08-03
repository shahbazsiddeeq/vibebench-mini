class Singleton:
    """Singleton class ensuring only one instance exists per process."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def reset(cls):
        """Discard the cached instance so the next call creates a fresh one."""
        cls._instance = None
