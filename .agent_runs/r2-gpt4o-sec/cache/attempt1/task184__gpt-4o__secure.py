class Peekable:
    def __init__(self, iterable):
        try:
            self._iterator = iter(iterable)
        except TypeError:
            raise TypeError("Provided object is not iterable")
        self._has_peeked = False
        self._peeked_value = None

    def __iter__(self):
        return self

    def __next__(self):
        if self._has_peeked:
            self._has_peeked = False
            return self._peeked_value
        return next(self._iterator)

    def peek(self, default=None):
        if not self._has_peeked:
            try:
                self._peeked_value = next(self._iterator)
                self._has_peeked = True
            except StopIteration:
                if default is None:
                    raise
                return default
        return self._peeked_value

    def has_next(self):
        if self._has_peeked:
            return True
        try:
            self._peeked_value = next(self._iterator)
            self._has_peeked = True
            return True
        except StopIteration:
            return False
