"""
Singleton Pattern Implementation

This module provides a Singleton class that ensures only one instance exists
per process. The instance can be reset for testing purposes.
"""

import threading
from typing import Optional


class Singleton:
    """
    A singleton class that ensures only one instance exists per process.
    
    Calling Singleton() always returns the same instance unless reset() is called.
    The reset() class method discards the cached instance so the next Singleton()
    call creates a fresh one (intended for tests).
    
    Note: __init__ may re-run on each Singleton() call, so do not rely on
    one-time initialization.
    """
    
    _instance: Optional['Singleton'] = None
    _lock: threading.Lock = threading.Lock()
    
    def __new__(cls) -> 'Singleton':
        """
        Create or return the singleton instance.
        
        Uses double-checked locking pattern for thread safety.
        """
        if cls._instance is None:
            with cls._lock:
                # Double-check after acquiring lock
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def reset(cls) -> None:
        """
        Reset the singleton instance.
        
        Discards the cached instance so the next Singleton() call creates
        a fresh one. This is intended for testing purposes.
        """
        with cls._lock:
            cls._instance = None
