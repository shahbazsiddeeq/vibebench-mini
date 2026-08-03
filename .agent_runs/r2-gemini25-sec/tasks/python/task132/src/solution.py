import collections
import threading
from typing import Callable, List, Any


class _Task:
    """Internal class to hold a callable and its result/exception."""

    def __init__(self, index: int, fn: Callable[[], Any]):
        self.index = index
        self.fn = fn
        self.result: Any = None
        self.exception: Exception | None = None
        self.done = threading.Event()

    def run(self):
        """Executes the callable and stores its result or exception."""
        try:
            self.result = self.fn()
        except Exception as e:
            self.exception = e
        finally:
            self.done.set()


def run_bounded(fns: List[Callable[[], Any]], max_concurrent: int) -> List[Any]:
    """
    Runs the zero-arg callables in `fns` using threads with at most max_concurrent
    running at once, and returns their results in the order of `fns`.

    Args:
        fns: A list of zero-argument callable functions.
        max_concurrent: The maximum number of concurrent threads allowed.
                        Must be greater than or equal to 1.

    Returns:
        A list containing the results of the functions, in the same order
        as the input `fns`.

    Raises:
        ValueError: If `max_concurrent` is less than 1.
        Exception: If any of the executed functions raise an exception,
                   that exception will be re-raised by this function.
    """
    if not isinstance(fns, list):
        raise TypeError("fns must be a list of callables.")
    if not all(callable(f) for f in fns):
        raise TypeError("All elements in fns must be callable.")
    if not isinstance(max_concurrent, int):
        raise TypeError("max_concurrent must be an integer.")
    if max_concurrent < 1:
        raise ValueError("max_concurrent must be greater than or equal to 1.")

    if not fns:
        return []

    # Use a deque for efficient popping from the left
    tasks_to_run = collections.deque([_Task(i, fn) for i, fn in enumerate(fns)])
    results: List[Any | None] = [None] * len(fns)
    
    # Semaphore to limit concurrent threads
    semaphore = threading.Semaphore(max_concurrent)
    
    # List to keep track of active threads
    active_threads: List[threading.Thread] = []

    def worker():
        """Worker function for each thread."""
        while True:
            task: _Task | None = None
            # Acquire semaphore before trying to get a task
            semaphore.acquire()
            try:
                # Safely get a task from the deque
                with threading.Lock(): # Protect access to tasks_to_run
                    if tasks_to_run:
                        task = tasks_to_run.popleft()
                    else:
                        # No more tasks, release semaphore and exit
                        semaphore.release()
                        break
                
                task.run()
                
                # Store result or re-raise exception
                if task.exception:
                    # If an exception occurred, we need to propagate it.
                    # For now, we store it and will re-raise after all threads
                    # have finished or been signaled to stop.
                    # A more sophisticated approach might involve a shared
                    # exception queue and immediate termination.
                    pass # Exception will be checked later
                else:
                    results[task.index] = task.result
            finally:
                # Ensure semaphore is released even if task.run() fails
                if task: # Only release if a task was actually picked up
                    semaphore.release()
                elif not tasks_to_run: # If no task was picked and queue is empty, worker should exit
                    break

    # Start worker threads
    for _ in range(max_concurrent):
        thread = threading.Thread(target=worker)
        thread.daemon = True # Allow program to exit even if threads are stuck
        thread.start()
        active_threads.append(thread)

    # Wait for all tasks to be processed.
    # This loop ensures that all tasks are eventually picked up and processed
    # by the worker threads. The semaphore ensures concurrency limits.
    # We wait for all threads to finish.
    for thread in active_threads:
        thread.join()

    # After all threads have finished, check for any exceptions
    for task in (t for t in tasks_to_run if t.done.is_set()): # Check tasks that might have been processed before queue emptied
        if task.exception:
            raise task.exception
    
    # Re-iterate through the original fns to find the corresponding _Task objects
    # and check for exceptions. This is necessary because tasks_to_run might be empty
    # but some tasks might have completed with exceptions.
    # A more robust solution would be to store all _Task objects in a list
    # and iterate over that list at the end.
    # For simplicity and to avoid re-creating the list, we can assume that
    # if an exception occurred, it would have been stored in the `_Task` object
    # that was processed.
    # The current implementation of `worker` doesn't explicitly store exceptions
    # in a shared list, so we need to ensure that if an exception happens,
    # it's caught and re-raised.
    # The `_Task` objects are created at the beginning. Let's ensure we can
    # access them all to check for exceptions.
    
    # A better way to manage tasks and results:
    all_tasks = [_Task(i, fn) for i, fn in enumerate(fns)]
    tasks_queue = collections.deque(all_tasks) # Use this for workers to pick from

    # Reset semaphore and threads for the corrected logic
    semaphore = threading.Semaphore(max_concurrent)
    active_threads = []
    
    def worker_corrected():
        while True:
            semaphore.acquire()
            task: _Task | None = None
            try:
                with threading.Lock(): # Protect access to tasks_queue
                    if tasks_queue:
                        task = tasks_queue.popleft()
                    else:
                        break # No more tasks
                
                task.run()
                # Result/exception is stored directly in the task object
            finally:
                semaphore.release()
                if not task and not tasks_queue: # If no task was picked and queue is empty, worker should exit
                    break

    for _ in range(max_concurrent):
        thread = threading.Thread(target=worker_corrected)
        thread.daemon = True
        thread.start()
        active_threads.append(thread)

    for thread in active_threads:
        thread.join()

    # Collect results and re-raise any exceptions
    final_results: List[Any] = [None] * len(fns)
    for task in all_tasks:
        if task.exception:
            raise task.exception
        final_results[task.index] = task.result

    return final_results
