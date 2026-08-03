"""
src/solution.py

Provides `parallel_map`: an order-preserving parallel map implementation
using a bounded thread pool.

Security / robustness notes:
- Inputs are validated defensively (types, ranges) before use.
- No use of eval/exec or dynamic code execution.
- No external I/O; errors raised are generic ValueError/TypeError without
  leaking internal state or stack details beyond what Python normally
  provides.
- Uses concurrent.futures.ThreadPoolExecutor from the standard library to
  bound resource usage (thread count) explicitly via `workers`.
"""

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Iterable, List


def parallel_map(fn: Callable[[Any], Any], items: Iterable[Any], workers: int = 4) -> List[Any]:
    """
    Apply `fn` to each item in `items` concurrently using up to `workers`
    threads, returning results in the same order as the input items.

    Args:
        fn: A callable taking a single argument and returning a result.
        items: An iterable of items to process.
        workers: Number of worker threads to use (must be >= 1).

    Returns:
        A list of results, in the same order as `items`.

    Raises:
        TypeError: If `fn` is not callable or `items` is not iterable.
        ValueError: If `workers` is not a positive integer.
    """
    if not callable(fn):
        raise TypeError("fn must be callable")

    if isinstance(workers, bool) or not isinstance(workers, int):
        raise ValueError("workers must be a positive integer")
    if workers < 1:
        raise ValueError("workers must be >= 1")

    try:
        items_list = list(items)
    except TypeError as exc:
        raise TypeError("items must be iterable") from exc

    if not items_list:
        return []

    n = len(items_list)
    # No need to spin up more workers than tasks.
    effective_workers = min(workers, n)

    results: List[Any] = [None] * n

    def _run(index: int, value: Any) -> None:
        results[index] = fn(value)

    with ThreadPoolExecutor(max_workers=effective_workers) as executor:
        futures = [
            executor.submit(_run, idx, val) for idx, val in enumerate(items_list)
        ]
        # Propagate exceptions (if any) from worker threads.
        for future in futures:
            future.result()

    return results
