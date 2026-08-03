from __future__ import annotations

_MISSING = object()


class Peekable:
    """An iterator wrapper that supports one-element look-ahead."""

    def __init__(self, iterable) -> None:
        try:
            self._it = iter(iterable)
        except TypeError:
            raise TypeError("Peekable requires an iterable")
        self._cache = _MISSING  # holds a peeked-but-not-yet-consumed item

    def __iter__(self) -> "Peekable":
        return self

    def __next__(self):
        if self._cache is not _MISSING:
            value = self._cache
            self._cache = _MISSING
            return value
        return next(self._it)

    def peek(self, default=_MISSING):
        if self._cache is _MISSING:
            try:
                self._cache = next(self._it)
            except StopIteration:
                if default is _MISSING:
                    raise
                return default
        return self._cache

    def has_next(self) -> bool:
        try:
            self.peek()
        except StopIteration:
            return False
        return True
