def chunked(iterable, size):
    """
    Yields successive chunks of up to size elements as lists.
    
    Args:
        iterable: An iterable to chunk
        size: The size of each chunk
        
    Yields:
        Lists of up to size elements from the iterable
        
    Raises:
        ValueError: If size < 1
    """
    if not isinstance(size, int) or size < 1:
        raise ValueError("size must be an integer >= 1")
    
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
