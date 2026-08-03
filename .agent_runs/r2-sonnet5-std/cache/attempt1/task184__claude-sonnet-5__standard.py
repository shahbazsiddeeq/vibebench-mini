_SENTINEL = object()


class Peekable:
    def __init__(self, iterable):
        self._it = iter(iterable)
        self._cache = _SENTINEL

    def __iter__(self):
        return self

    def __next__(self):
        if self._cache is not _SENTINEL:
            value = self._cache
            self._cache = _SENTINEL
            return value
        return next(self._it)

    def peek(self, default=_SENTINEL):
        if self._cache is _SENTINEL:
            try:
                self._cache = next(self._it)
            except StopIteration:
                if default is _SENTINEL:
                    raise
                return default
        return self._cache

    def has_next(self):
        if self._cache is not _SENTINEL:
            return True
        try:
            self._cache = next(self._it)
        except StopIteration:
            return False
        return True
