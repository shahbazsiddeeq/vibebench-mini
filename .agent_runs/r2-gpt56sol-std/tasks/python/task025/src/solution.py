from typing import TypeVar

T = TypeVar("T")


def rotate(lst: list[T], k: int) -> list[T]:
    """Return a new list containing the elements of *lst* rotated right by *k*."""
    if not lst:
        return []

    offset = k % len(lst)
    if offset == 0:
        return list(lst)

    return lst[-offset:] + lst[:-offset]
