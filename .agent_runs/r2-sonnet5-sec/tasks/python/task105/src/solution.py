"""
Producer-Consumer Queue implementation.

Provides `produce_consume`, a thread-based utility that applies a
processing function to a collection of items using a bounded number of
worker threads, while preserving the original input order in the
returned results.

The implementation is careful about:
    * Validating all inputs (types, ranges) before doing any work.
    * Never using eval/exec or other dynamic code execution.
    * Using thread-safe primitives (queue.Queue) for coordination.
    * Not leaking internal exception details (tracebacks, file paths,
      etc.) to the caller; only a sanitized error message is surfaced.
"""

from __future__ import annotations

import queue
import threading
from typing import Any, Callable, Iterable, List


def produce_consume(
    items: Iterable[Any],
    process_fn: Callable[[Any], Any],
    n_workers: int = 2,
) -> List[Any]:
    """
    Apply `process_fn` to each item in `items` using `n_workers` threads.

    Results are returned in the same order as the input items, regardless
    of the order in which the worker threads complete their work.

    Args:
        items: An iterable of items to process. Consumed eagerly into a
            list to determine the number of results and their order.
        process_fn: A callable taking a single argument and returning a
            result. Must be callable.
        n_workers: Number of worker threads to use. Must be an integer
            >= 1.

    Returns:
        A list of results, in the same order as the input items.

    Raises:
        ValueError: If `n_workers` is not a positive integer, or if
            `process_fn` is not callable.
        RuntimeError: If an error occurs while processing an item; the
            original exception details are not exposed, only a generic
            sanitized message.
    """
    # --- Input validation -------------------------------------------------
    if not isinstance(n_workers, int) or isinstance(n_workers, bool):
        raise ValueError("n_workers must be an integer")
    if n_workers < 1:
        raise ValueError("n_workers must be >= 1")

    if not callable(process_fn):
        raise ValueError("process_fn must be callable")

    # Materialize items safely; if this fails (e.g. not iterable), raise
    # a clear, sanitized error instead of letting a raw exception escape.
    try:
        item_list = list(items)
    except TypeError as exc:
        raise ValueError("items must be iterable") from exc

    n_items = len(item_list)
    if n_items == 0:
        return []

    # Clamp worker count so we never spin up more threads than items.
    effective_workers = min(n_workers, n_items)

    # --- Setup queues and result storage -----------------------------------
    task_queue: "queue.Queue[Any]" = queue.Queue()
    results: List[Any] = [None] * n_items
    error_holder: List[BaseException] = []
    error_lock = threading.Lock()

    for index, item in enumerate(item_list):
        task_queue.put((index, item))

    # Sentinel values, one per worker, to signal shutdown.
    for _ in range(effective_workers):
        task_queue.put(None)

    def worker() -> None:
        while True:
            task = task_queue.get()
            try:
                if task is None:
                    return
                index, item = task
                try:
                    result = process_fn(item)
                except Exception as exc:  # noqa: BLE001 - intentional broad catch
                    with error_lock:
                        # Store only a sanitized message, not the raw
                        # exception object with potentially sensitive
                        # internal details/tracebacks.
                        if not error_holder:
                            error_holder.append(
                                RuntimeError(
                                    "Error processing item at index "
                                    f"{index}: processing failed"
                                )
                            )
                    continue
                results[index] = result
            finally:
                task_queue.task_done()

    threads = [
        threading.Thread(target=worker, daemon=True)
        for _ in range(effective_workers)
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    if error_holder:
        raise error_holder[0]

    return results
