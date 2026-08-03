def chunked(iterable, size):
    if size < 1:
        raise ValueError("size must be at least 1")

    it = iter(iterable)
    while True:
        chunk = []
        try:
            for _ in range(size):
                chunk.append(next(it))
            yield chunk
        except StopIteration:
            if chunk:  # Yield any remaining elements as the last chunk
                yield chunk
            return
