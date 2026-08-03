from typing import Any, Iterable, Iterator, TypeVar, Generic, overload

T = TypeVar("T")
D = TypeVar("D")

_MISSING = object()


class Peekable(Generic[T], Iterator[T]):
    """An iterator wrapper providing one-item look-ahead."""

    def __init__(self, iterable: Iterable[T]) -> None:
        self._iterator = iter(iterable)
        self._buffer: Any = _MISSING

    def __iter__(self) -> "Peekable[T]":
        return self

    def __next__(self) -> T:
        if self._buffer is not _MISSING:
            item = self._buffer
            self._buffer = _MISSING
            return item
        return next(self._iterator)

    def _fill(self) -> bool:
        if self._buffer is not _MISSING:
            return True
        try:
            self._buffer = next(self._iterator)
        except StopIteration:
            return False
        return True

    @overload
    def peek(self) -> T:
        ...

    @overload
    def peek(self, default: D) -> T | D:
        ...

    def peek(self, default: Any = _MISSING) -> Any:
        if self._fill():
            return self._buffer
        if default is _MISSING:
            raise StopIteration
        return default

    def has_next(self) -> bool:
        return self._fill()
