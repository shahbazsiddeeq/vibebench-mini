# src/solution.py

class Peekable:
    def __init__(self, iterable):
        try:
            self._iterator = iter(iterable)
        except TypeError:
            raise TypeError("The provided argument is not iterable.")
        
        self._buffer = None
        self._has_buffer = False

    def __iter__(self):
        return self

    def __next__(self):
        if self._has_buffer:
            self._has_buffer = False
            return self._buffer
        
        try:
            return next(self._iterator)
        except StopIteration:
            raise

    def peek(self, default=None):
        if self._has_buffer:
            return self._buffer
        
        try:
            self._buffer = next(self._iterator)
            self._has_buffer = True
            return self._buffer
        except StopIteration:
            if default is not None:
                return default
            raise

    def has_next(self):
        if self._has_buffer:
            return True
        
        try:
            self._buffer = next(self._iterator)
            self._has_buffer = True
            return True
        except StopIteration:
            return False
