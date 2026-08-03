"""
src/solution.py

A thread-safe Singleton pattern implementation.

Design notes:
- Uses a class-level lock to guard instance creation against race
  conditions in multi-threaded contexts.
- reset() discards the cached instance (intended for test isolation),
  so the next call to Singleton() will construct a fresh instance.
- Subclasses each get their own instance slot (per-class __dict__),
  since the instance is stored on the class itself via cls, not on a
  hardcoded base class attribute.
- __init__ may run again on every Singleton() call (standard Python
  object construction behavior when __new__ returns an existing
  instance is that __init__ still executes), so no code here should
  assume one-time initialization semantics beyond what's documented.
"""

import threading
from typing import Any


class Singleton:
    """A simple, thread-safe singleton base class.

    Usage:
        a = Singleton()
        b = Singleton()
        assert a is b

        Singleton.reset()
        c = Singleton()
        assert c is not a
    """

    _instance: Any = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls, *args: Any, **kwargs: Any) -> "Singleton":
        # Double-checked locking for thread safety without paying the
        # lock overhead on every call once the instance exists.
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Discard the cached instance.

        After calling this, the next call to Singleton() (or a
        subclass constructor) will create and cache a brand new
        instance.
        """
        with cls._lock:
            cls._instance = None
