"""
Thread-safe counter implementation.

This module provides an AtomicCounter class that supports safe concurrent
increment, decrement, and value retrieval operations using a threading lock
to guarantee atomicity of read-modify-write sequences.
"""

import threading
from typing import Union


class AtomicCounter:
    """
    A thread-safe counter supporting atomic increment, decrement, and value
    retrieval operations.

    Attributes:
        _value (int): The internal counter value.
        _lock (threading.Lock): Lock guarding all mutations/reads of _value.
    """

    __slots__ = ("_value", "_lock")

    def __init__(self, initial: int = 0) -> None:
        """
        Initialize the counter.

        Args:
            initial: The starting value for the counter. Must be a
                non-negative integer.

        Raises:
            ValueError: If initial is not an integer or is negative.
        """
        if isinstance(initial, bool) or not isinstance(initial, int):
            raise ValueError("initial must be an integer")
        if initial < 0:
            raise ValueError("initial must be non-negative")

        self._value = initial
        self._lock = threading.Lock()

    def increment(self) -> int:
        """
        Atomically increment the counter by 1.

        Returns:
            The new value of the counter after incrementing.
        """
        with self._lock:
            self._value += 1
            return self._value

    def decrement(self) -> int:
        """
        Atomically decrement the counter by 1.

        Returns:
            The new value of the counter after decrementing.
        """
        with self._lock:
            self._value -= 1
            return self._value

    def value(self) -> int:
        """
        Atomically retrieve the current value of the counter.

        Returns:
            The current value of the counter.
        """
        with self._lock:
            return self._value
