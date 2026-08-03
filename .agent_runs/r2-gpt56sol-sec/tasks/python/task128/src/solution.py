from __future__ import annotations

import operator
from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor
from typing import Any, TypeVar


T = TypeVar("T")
R = TypeVar("R")


def parallel_map(
    fn: Callable[[T], R],
    items: Iterable[T],
    workers: int = 4,
) -> list[R]:
    """Apply ``fn`` concurrently and return results in input order."""
    if not callable(fn):
        raise TypeError("fn must be callable")

    try:
        worker_count = operator.index(workers)
    except TypeError:
        raise TypeError("workers must be an integer") from None

    if worker_count < 1:
        raise ValueError("workers must be at least 1")

    try:
        iterator = iter(items)
    except TypeError:
        raise TypeError("items must be iterable") from None

    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        return list(executor.map(fn, iterator))
