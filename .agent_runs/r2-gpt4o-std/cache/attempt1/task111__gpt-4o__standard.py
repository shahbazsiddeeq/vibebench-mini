def chunked(iterable, size):
    if size < 1:
        raise ValueError("Size must be at least 1")
    
    iterator = iter(iterable)
    while True:
        chunk = list(itertools.islice(iterator, size))
        if not chunk:
            break
        yield chunk
