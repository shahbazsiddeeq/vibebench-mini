import queue
import threading
from typing import Callable

# Unique sentinel so that None items in `items` never collide with the
# shutdown signal placed on the queue.
_SHUTDOWN = object()


def produce_consume(items: list, process_fn: Callable, n_workers: int = 2) -> list:
    """Apply process_fn to each item using n_workers threads via queue.Queue.

    Results are returned in the SAME order as the input items. Raises
    ValueError if n_workers < 1.
    """
    if n_workers < 1:
        raise ValueError("n_workers must be >= 1")

    q: queue.Queue = queue.Queue()
    results = [None] * len(items)

    # Enqueue indexed work so results can be placed back in input order.
    for idx, item in enumerate(items):
        q.put((idx, item))
    for _ in range(n_workers):
        q.put(_SHUTDOWN)

    def worker() -> None:
        while True:
            task = q.get()
            if task is _SHUTDOWN:
                break
            idx, item = task
            results[idx] = process_fn(item)

    threads = [threading.Thread(target=worker) for _ in range(n_workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return results
