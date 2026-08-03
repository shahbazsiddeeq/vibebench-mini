"""Threaded producer-consumer utilities."""

from queue import Queue
from threading import Thread
from typing import Callable, Iterable, TypeVar

T = TypeVar("T")
R = TypeVar("R")


def produce_consume(
    items: Iterable[T],
    process_fn: Callable[[T], R],
    n_workers: int = 2,
) -> list[R]:
    """Apply process_fn to each item using worker threads.

    Results are returned in the same order as the input items.
    """
    if n_workers < 1:
        raise ValueError("n_workers must be at least 1")

    input_items = list(items)
    if not input_items:
        return []

    tasks: Queue[object] = Queue()
    sentinel = object()
    missing = object()
    results: list[object] = [missing] * len(input_items)
    errors: list[BaseException | None] = [None] * len(input_items)

    def worker() -> None:
        while True:
            task = tasks.get()
            try:
                if task is sentinel:
                    return

                index, item = task  # type: ignore[misc]
                try:
                    results[index] = process_fn(item)
                except BaseException as exc:
                    errors[index] = exc
            finally:
                tasks.task_done()

    workers = [Thread(target=worker) for _ in range(n_workers)]
    for thread in workers:
        thread.start()

    for index, item in enumerate(input_items):
        tasks.put((index, item))

    for _ in workers:
        tasks.put(sentinel)

    tasks.join()

    for thread in workers:
        thread.join()

    for error in errors:
        if error is not None:
            raise error

    return results  # type: ignore[return-value]
