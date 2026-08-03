import queue
import threading


def produce_consume(items, process_fn, n_workers=2):
    if n_workers < 1:
        raise ValueError("n_workers must be >= 1")

    items = list(items)
    if not items:
        return []

    task_queue = queue.Queue()
    results = [None] * len(items)

    for idx, item in enumerate(items):
        task_queue.put((idx, item))

    def worker():
        while True:
            try:
                idx, item = task_queue.get_nowait()
            except queue.Empty:
                return
            results[idx] = process_fn(item)
            task_queue.task_done()

    threads = []
    for _ in range(n_workers):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return results
