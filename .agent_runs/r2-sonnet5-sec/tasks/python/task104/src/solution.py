"""
Strategy Pattern (Sorter) module.

This module provides a Sorter class implementing the Strategy design
pattern for sorting, along with two concrete sorting strategy
functions: bubble_sort and insertion_sort.

Security considerations:
- All inputs are validated (must be lists) before processing.
- No use of eval/exec or other dangerous constructs.
- Sorting functions never mutate their input; they operate on a copy.
- Errors are raised with generic, safe messages that do not leak
  internal state or implementation details.
"""

from typing import Any, Callable, List


def _validate_list(data: Any) -> List[Any]:
    """
    Validate that `data` is a list, and return a shallow copy of it.

    Raises:
        TypeError: if `data` is not a list.
    """
    if not isinstance(data, list):
        raise TypeError("Input must be a list.")
    return list(data)


def bubble_sort(lst: List[Any]) -> List[Any]:
    """
    Return a new list with elements of `lst` sorted in ascending order,
    using the bubble sort algorithm. Does not mutate the input list.

    Args:
        lst: A list of comparable elements.

    Returns:
        A new sorted list.

    Raises:
        TypeError: if `lst` is not a list.
    """
    result = _validate_list(lst)
    n = len(result)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:
            break
    return result


def insertion_sort(lst: List[Any]) -> List[Any]:
    """
    Return a new list with elements of `lst` sorted in ascending order,
    using the insertion sort algorithm. Does not mutate the input list.

    Args:
        lst: A list of comparable elements.

    Returns:
        A new sorted list.

    Raises:
        TypeError: if `lst` is not a list.
    """
    result = _validate_list(lst)
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result


class Sorter:
    """
    A context class for the Strategy pattern that delegates sorting
    to a configurable strategy function.

    The strategy must be a callable that accepts a list and returns
    a new sorted list without mutating its argument.
    """

    def __init__(self, strategy: Callable[[List[Any]], List[Any]]) -> None:
        self.set_strategy(strategy)

    def set_strategy(self, strategy: Callable[[List[Any]], List[Any]]) -> None:
        """
        Replace the current sorting strategy.

        Args:
            strategy: A callable taking a list and returning a new
                sorted list.

        Raises:
            TypeError: if `strategy` is not callable.
        """
        if not callable(strategy):
            raise TypeError("Strategy must be callable.")
        self._strategy = strategy

    def sort(self, data: List[Any]) -> List[Any]:
        """
        Sort `data` using the current strategy, returning a new list.
        The original `data` list is never mutated.

        Args:
            data: A list of comparable elements.

        Returns:
            A new sorted list produced by the current strategy.

        Raises:
            TypeError: if `data` is not a list.
            RuntimeError: if the strategy fails during execution.
        """
        validated = _validate_list(data)
        try:
            result = self._strategy(validated)
        except TypeError:
            raise
        except Exception as exc:
            raise RuntimeError("Sorting strategy failed.") from exc

        if not isinstance(result, list):
            raise TypeError("Strategy did not return a list.")

        return result
