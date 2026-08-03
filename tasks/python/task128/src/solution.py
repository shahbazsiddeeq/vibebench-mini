from concurrent.futures import ThreadPoolExecutor


def parallel_map(fn, items: list, workers: int = 4) -> list:
    """Apply fn to each item using up to `workers` threads, preserving input order."""
    if workers < 1:
        raise ValueError("workers must be >= 1")
    if not items:
        return []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        # executor.map yields results in the order the inputs were submitted.
        return list(executor.map(fn, items))
