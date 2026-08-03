import threading
import queue
from typing import List, Callable, Any
import secrets

def produce_consume(items: List[Any], process_fn: Callable[[Any], Any], n_workers: int = 2) -> List[Any]:
    if n_workers < 1:
        raise ValueError("Number of workers must be at least 1")

    task_queue = queue.Queue()
    result_queue = queue.Queue()
    results = [None] * len(items)
    lock = threading.Lock()

    def worker():
        while True:
            index, item = task_queue.get()
            if item is None:
                break
            try:
                result = process_fn(item)
                with lock:
                    results[index] = result
            finally:
                task_queue.task_done()

    threads = []
    for _ in range(n_workers):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    for index, item in enumerate(items):
        task_queue.put((index, item))

    task_queue.join()

    for _ in range(n_workers):
        task_queue.put((None, None))

    for thread in threads:
        thread.join()

    return results
