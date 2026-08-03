from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable, TypeVar

T = TypeVar("T")


def run_bounded(
    fns: Iterable[Callable[[], T]], max_concurrent: int
) -> list[T]:
    """Run zero-argument callables with bounded thread concurrency.

    Results are returned in the same order as the supplied callables.
    """
    if not isinstance(max_concurrent, int) or isinstance(max_concurrent, bool):
        raise ValueError("max_concurrent must be an integer of at least 1")
    if max_concurrent < 1:
        raise ValueError("max_concurrent must be at least 1")

    functions = list(fns)
    if not functions:
        return []

    with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        return list(executor.map(lambda fn: fn(), functions))
