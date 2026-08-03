import threading
import queue

def produce_consume(items, process_fn, n_workers=2):
    if not isinstance(n_workers, int) or n_workers < 1:
        raise ValueError("n_workers must be a positive integer.")
    
    results = [None] * len(items)
    item_queue = queue.Queue()
    result_queue = queue.Queue()

    def worker():
        while True:
            index, item = item_queue.get()
            if item is None:
                break
            result = process_fn(item)
            result_queue.put((index, result))
            item_queue.task_done()

    threads = []
    for _ in range(n_workers):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    for index, item in enumerate(items):
        item_queue.put((index, item))

    # Stop workers
    for _ in threads:
        item_queue.put((None, None))

    item_queue.join()

    while not result_queue.empty():
        index, result = result_queue.get()
        results[index] = result

    for thread in threads:
        thread.join()

    return results
