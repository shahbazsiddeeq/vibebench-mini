def chunked(iterable, size):
    if size < 1:
        raise ValueError("size must be >= 1")

    def generator():
        it = iter(iterable)
        while True:
            chunk = []
            for _ in range(size):
                try:
                    chunk.append(next(it))
                except StopIteration:
                    if chunk:
                        yield chunk
                    return
            yield chunk

    return generator()
