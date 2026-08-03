"""Bounded concurrency executor module."""

from concurrent.futures import ThreadPoolExecutor


def run_bounded(fns, max_concurrent):
    """Run zero-arg callables in fns with at most max_concurrent threads.

    Returns results in the same order as fns.
    Raises ValueError if max_concurrent < 1.
    """
    if max_concurrent < 1:
        raise ValueError("max_concurrent must be >= 1")

    if not fns:
        return []

    with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        futures = [executor.submit(fn) for fn in fns]
        results = [f.result() for f in futures]

    return results
