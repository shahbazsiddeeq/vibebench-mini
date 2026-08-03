import threading
from queue import Queue
from typing import Callable, List, Any

def parallel_map(fn: Callable[[Any], Any], items: List[Any], workers: int = 4) -> List[Any]:
    if workers < 1:
        raise ValueError("Number of workers must be at least 1")
    
    if not items:
        return []

    result = [None] * len(items)
    queue = Queue()

    def worker():
        while True:
            index, item = queue.get()
            if index is None:
                break
            result[index] = fn(item)
            queue.task_done()

    threads = []
    for _ in range(workers):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    for index, item in enumerate(items):
        queue.put((index, item))

    queue.join()

    for _ in range(workers):
        queue.put((None, None))

    for thread in threads:
        thread.join()

    return result
