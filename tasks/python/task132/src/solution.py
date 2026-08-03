from concurrent.futures import ThreadPoolExecutor


def run_bounded(fns: list, max_concurrent: int) -> list:
    """Run zero-arg callables with at most max_concurrent running at once.

    Results are returned in the same order as `fns`.
    """
    if max_concurrent < 1:
        raise ValueError("max_concurrent must be >= 1")
    if not fns:
        return []
    with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        futures = [executor.submit(fn) for fn in fns]
        return [f.result() for f in futures]
