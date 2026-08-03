"""Sorting strategies and a context implementing the Strategy pattern."""

from collections.abc import Callable
from typing import Any


def _validate_list(value: Any, name: str) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be a list")


def bubble_sort(lst: list[Any]) -> list[Any]:
    """Return a bubble-sorted copy of *lst* without modifying *lst*."""
    _validate_list(lst, "lst")
    result = lst.copy()

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


def insertion_sort(lst: list[Any]) -> list[Any]:
    """Return an insertion-sorted copy of *lst* without modifying *lst*."""
    _validate_list(lst, "lst")
    result = lst.copy()

    for index in range(1, len(result)):
        value = result[index]
        position = index

        while position > 0 and result[position - 1] > value:
            result[position] = result[position - 1]
            position -= 1

        result[position] = value

    return result


class Sorter:
    """Sort lists using a replaceable sorting strategy."""

    def __init__(self, strategy: Callable[[list[Any]], list[Any]]) -> None:
        self.set_strategy(strategy)

    def set_strategy(
        self, strategy: Callable[[list[Any]], list[Any]]
    ) -> None:
        """Replace the current sorting strategy."""
        if not callable(strategy):
            raise TypeError("strategy must be callable")
        self.strategy = strategy

    def sort(self, data: list[Any]) -> list[Any]:
        """Return a sorted copy of *data* using the current strategy."""
        _validate_list(data, "data")

        result = self.strategy(data.copy())
        if not isinstance(result, list):
            raise TypeError("strategy must return a list")

        return result.copy()


__all__ = ["Sorter", "bubble_sort", "insertion_sort"]
