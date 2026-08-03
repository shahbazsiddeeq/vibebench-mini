import threading

class AtomicCounter:
    """
    A thread-safe counter that supports atomic increment, decrement, and value retrieval.
    """

    def __init__(self, initial: int = 0):
        """
        Initializes the AtomicCounter with an optional initial value.

        Args:
            initial: The starting value for the counter. Must be a non-negative integer.

        Raises:
            ValueError: If the initial value is negative or not an integer.
        """
        if not isinstance(initial, int):
            raise ValueError("Initial value must be an integer.")
        if initial < 0:
            raise ValueError("Initial value cannot be negative.")

        self._value = initial
        self._lock = threading.Lock()

    def increment(self) -> int:
        """
        Atomically increments the counter's value by 1.

        Returns:
            The new value of the counter after the increment.
        """
        with self._lock:
            self._value += 1
            return self._value

    def decrement(self) -> int:
        """
        Atomically decrements the counter's value by 1.

        Returns:
            The new value of the counter after the decrement.
        """
        with self._lock:
            self._value -= 1
            return self._value

    def value(self) -> int:
        """
        Atomically retrieves the current value of the counter.

        Returns:
            The current value of the counter.
        """
        with self._lock:
            return self._value
