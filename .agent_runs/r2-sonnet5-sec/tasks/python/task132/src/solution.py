"""
src/solution.py

A small, security-conscious bounded-concurrency executor.

run_bounded(fns, max_concurrent) executes a sequence of zero-argument
callables using a bounded number of worker threads and returns their
results in the same order as the input sequence.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, List, Sequence


class TaskExecutionError(RuntimeError):
    """Raised when one or more submitted callables raise an exception.

    The original exception is intentionally not exposed in the message to
    avoid leaking internal details; it is available via __cause__.
    """


def run_bounded(fns: Sequence[Callable[[], Any]], max_concurrent: int) -> List[Any]:
    """
    Run the zero-argument callables in `fns` using at most `max_concurrent`
    threads concurrently, returning their results in the same order as
    `fns`.

    Args:
        fns: A sequence of zero-argument callables.
        max_concurrent: Maximum number of threads allowed to run at once.
                         Must be an integer >= 1.

    Returns:
        A list of results corresponding to each callable in `fns`, in the
        same order as the input.

    Raises:
        ValueError: If max_concurrent is not an integer >= 1, or if `fns`
                    is not a valid sequence, or if any element of `fns`
                    is not callable.
        TaskExecutionError: If any callable raises an exception during
                             execution.
    """
    # --- Input validation -------------------------------------------------
    if isinstance(max_concurrent, bool) or not isinstance(max_concurrent, int):
        raise ValueError("max_concurrent must be an integer")
    if max_concurrent < 1:
        raise ValueError("max_concurrent must be >= 1")

    if isinstance(fns, (str, bytes)):
        raise ValueError("fns must be a sequence of zero-argument callables")

    try:
        fns_list = list(fns)
    except TypeError as exc:
        raise ValueError("fns must be an iterable of zero-argument callables") from exc

    if not fns_list:
        return []

    for fn in fns_list:
        if not callable(fn):
            raise ValueError("All items in fns must be callable")

    # --- Execution ----------------------------------------------------------
    results: List[Any] = [None] * len(fns_list)
    errors: List[BaseException] = []

    def _wrap(index: int, fn: Callable[[], Any]) -> None:
        try:
            results[index] = fn()
        except BaseException as exc:  # noqa: BLE001 - intentionally broad to capture all task errors
            errors.append(exc)

    with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        futures = [
            executor.submit(_wrap, idx, fn) for idx, fn in enumerate(fns_list)
        ]
        for future in futures:
            future.result()

    if errors:
        raise TaskExecutionError(
            f"{len(errors)} task(s) raised an exception during execution"
        ) from errors[0]

    return results
