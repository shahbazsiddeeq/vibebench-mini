import threading

class Once:
    """
    A class that ensures a given callable is executed only once successfully,
    caching its result for all subsequent calls.
    """

    def __init__(self):
        """
        Initializes a Once object.
        """
        self._initialized = False
        self._result = None
        self._lock = threading.Lock()

    def do(self, fn):
        """
        Executes the provided callable `fn` only once successfully.

        If `fn` has already been successfully executed, its cached result is
        returned immediately. If `fn` has not been successfully executed yet,
        it is called. If `fn` completes successfully, its return value is
        cached and returned. If `fn` raises an exception, the exception
        propagates to the caller, and `fn` will be attempted again on
        subsequent calls to `do`.

        Args:
            fn: A zero-argument callable to be executed.

        Returns:
            The cached result of `fn`'s successful execution.

        Raises:
            TypeError: If `fn` is not a callable.
            Exception: Any exception raised by `fn`.
        """
        if not callable(fn):
            raise TypeError("Input 'fn' must be a callable.")

        # Fast path for already initialized state
        if self._initialized:
            return self._result

        with self._lock:
            # Double-checked locking: check again inside the lock
            if self._initialized:
                return self._result

            # Attempt to run the function
            # If fn raises an exception, it propagates out, and _initialized remains False.
            self._result = fn()
            self._initialized = True
            return self._result
