"""Threaded producer-consumer utilities."""

from __future__ import annotations

import queue
import threading
from typing import Callable, Iterable, TypeVar

_T = TypeVar("_T")
_R = TypeVar("_R")


def produce_consume(
    items: Iterable[_T],
    process_fn: Callable[[_T], _R],
    n_workers: int = 2,
) -> list[_R]:
    """Apply ``process_fn`` concurrently and return results in input order."""
    if not isinstance(n_workers, int):
        raise TypeError("n_workers must be an integer")
    if n_workers < 1:
        raise ValueError("n_workers must be at least 1")
    if not callable(process_fn):
        raise TypeError("process_fn must be callable")

    item_list = list(items)
    if not item_list:
        return []

    work_queue: queue.Queue[object] = queue.Queue()
    sentinel = object()
    results: list[object] = [None] * len(item_list)
    errors: list[BaseException | None] = [None] * len(item_list)

    def worker() -> None:
        while True:
            task = work_queue.get()
            try:
                if task is sentinel:
                    return

                index, item = task
                try:
                    results[index] = process_fn(item)
                except BaseException as exc:
                    errors[index] = exc
            finally:
                work_queue.task_done()

    worker_count = min(n_workers, len(item_list))
    threads = [
        threading.Thread(target=worker, daemon=True)
        for _ in range(worker_count)
    ]

    for thread in threads:
        thread.start()

    for index, item in enumerate(item_list):
        work_queue.put((index, item))
    for _ in threads:
        work_queue.put(sentinel)

    work_queue.join()
    for thread in threads:
        thread.join()

    for error in errors:
        if error is not None:
            raise error

    return results  # type: ignore[return-value]
