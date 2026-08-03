from typing import Generic, TypeVar

T = TypeVar("T")


class MinStack(Generic[T]):
    """A stack supporting constant-time minimum retrieval."""

    __slots__ = ("_items",)

    def __init__(self) -> None:
        self._items: list[tuple[T, T]] = []

    def push(self, val: T) -> None:
        if not self._items:
            current_min = val
        else:
            previous_min = self._items[-1][1]
            current_min = val if val < previous_min else previous_min
        self._items.append((val, current_min))

    def pop(self) -> T:
        if not self._items:
            raise IndexError("pop from empty MinStack")
        return self._items.pop()[0]

    def top(self) -> T:
        if not self._items:
            raise IndexError("top from empty MinStack")
        return self._items[-1][0]

    def get_min(self) -> T:
        if not self._items:
            raise IndexError("get_min from empty MinStack")
        return self._items[-1][1]
