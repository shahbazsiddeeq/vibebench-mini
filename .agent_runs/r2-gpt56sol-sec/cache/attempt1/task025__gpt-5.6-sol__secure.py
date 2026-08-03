from typing import TypeVar

T = TypeVar("T")


def rotate(lst: list[T], k: int) -> list[T]:
    """Return a new list rotated right by k positions."""
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    if not isinstance(k, int) or isinstance(k, bool):
        raise TypeError("k must be an integer")

    if not lst:
        return []

    offset = k % len(lst)
    if offset == 0:
        return lst.copy()

    return lst[-offset:] + lst[:-offset]
