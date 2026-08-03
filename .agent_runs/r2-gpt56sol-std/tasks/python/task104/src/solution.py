from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")
SortStrategy = Callable[[list[T]], list[T]]


def bubble_sort(lst: list[T]) -> list[T]:
    """Return a sorted copy of *lst* using bubble sort."""
    result = list(lst)

    for end in range(len(result) - 1, 0, -1):
        swapped = False
        for index in range(end):
            if result[index] > result[index + 1]:
                result[index], result[index + 1] = (
                    result[index + 1],
                    result[index],
                )
                swapped = True
        if not swapped:
            break

    return result


def insertion_sort(lst: list[T]) -> list[T]:
    """Return a sorted copy of *lst* using insertion sort."""
    result = list(lst)

    for index in range(1, len(result)):
        value = result[index]
        position = index

        while position > 0 and result[position - 1] > value:
            result[position] = result[position - 1]
            position -= 1

        result[position] = value

    return result


class Sorter:
    """Sort data using a replaceable sorting strategy."""

    def __init__(self, strategy: SortStrategy[Any]) -> None:
        self.strategy = strategy

    def sort(self, data: list[T]) -> list[T]:
        """Return a sorted copy of *data* without mutating it."""
        return self.strategy(list(data))

    def set_strategy(self, strategy: SortStrategy[Any]) -> None:
        """Replace the current sorting strategy."""
        self.strategy = strategy
