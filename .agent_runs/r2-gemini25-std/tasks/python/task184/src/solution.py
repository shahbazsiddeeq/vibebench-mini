class Peekable:
    def __init__(self, iterable):
        try:
            self._iterator = iter(iterable)
        except TypeError as e:
            raise TypeError("Argument must be iterable") from e
        self._buffer = []

    def __iter__(self):
        return self

    def __next__(self):
        if self._buffer:
            return self._buffer.pop(0)
        return next(self._iterator)

    def peek(self, default=None):
        if not self._buffer:
            try:
                next_item = next(self._iterator)
                self._buffer.append(next_item)
            except StopIteration:
                if default is not None:
                    return default
                raise
        return self._buffer[0]

    def has_next(self):
        if self._buffer:
            return True
        try:
            self.peek()
            return True
        except StopIteration:
            return False
