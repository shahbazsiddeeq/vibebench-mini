def chunked(iterable, size):
    """
    Yield successive chunks of up to size elements from iterable as lists.
    
    Args:
        iterable: An iterable to chunk
        size: Maximum number of elements per chunk
        
    Yields:
        Lists containing up to size elements
        
    Raises:
        ValueError: If size < 1
    """
    if size < 1:
        raise ValueError("size must be at least 1")
    
    iterator = iter(iterable)
    while True:
        chunk = []
        for _ in range(size):
            try:
                chunk.append(next(iterator))
            except StopIteration:
                if chunk:
                    yield chunk
                return
        yield chunk
