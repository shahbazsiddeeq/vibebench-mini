from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable, List, TypeVar

T = TypeVar("T")
R = TypeVar("R")


def parallel_map(
    fn: Callable[[T], R],
    items: Iterable[T],
    workers: int = 4,
) -> List[R]:
    if workers < 1:
        raise ValueError("workers must be at least 1")

    values = list(items)
    if not values:
        return []

    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(fn, values))
