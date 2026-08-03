# src/solution.py

import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

    @classmethod
    def reset(cls):
        with cls._lock:
            cls._instance = None
