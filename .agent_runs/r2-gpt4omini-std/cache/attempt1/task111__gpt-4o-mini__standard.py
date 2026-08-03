def chunked(iterable, size):
    if size < 1:
        raise ValueError("Size must be at least 1")
    
    iterator = iter(iterable)
    
    while True:
        chunk = list()
        try:
            for _ in range(size):
                chunk.append(next(iterator))
        except StopIteration:
            if chunk:
                yield chunk
            break
        yield chunk
