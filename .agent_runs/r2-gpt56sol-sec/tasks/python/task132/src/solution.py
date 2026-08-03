"""Utilities for executing callables with bounded thread concurrency."""

from concurrent.futures import ThreadPoolExecutor
import operator
from typing import Any, Callable, Iterable


def run_bounded(
    fns: Iterable[Callable[[], Any]], max_concurrent: int
) -> list[Any]:
    """Run zero-argument callables concurrently and return ordered results.

    At most ``max_concurrent`` callables execute simultaneously. If a callable
    raises an exception, that exception is propagated after all worker threads
    have been safely shut down.
    """
    if isinstance(max_concurrent, bool):
        raise ValueError("max_concurrent must be a positive integer")

    try:
        worker_limit = operator.index(max_concurrent)
    except TypeError as exc:
        raise ValueError("max_concurrent must be a positive integer") from exc

    if worker_limit < 1:
        raise ValueError("max_concurrent must be at least 1")

    try:
        tasks = list(fns)
    except TypeError as exc:
        raise TypeError("fns must be an iterable of callables") from exc

    if not all(callable(task) for task in tasks):
        raise TypeError("every item in fns must be callable")

    if not tasks:
        return []

    with ThreadPoolExecutor(max_workers=min(worker_limit, len(tasks))) as executor:
        futures = [executor.submit(task) for task in tasks]
        return [future.result() for future in futures]
