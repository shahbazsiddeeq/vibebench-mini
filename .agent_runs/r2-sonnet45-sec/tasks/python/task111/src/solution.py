def chunked(iterable, size):
    """
    Yield successive chunks of up to size elements from iterable as lists.
    
    Args:
        iterable: Any iterable to chunk
        size: Maximum number of elements per chunk (must be >= 1)
        
    Yields:
        Lists containing up to 'size' elements from the iterable
        
    Raises:
        ValueError: If size < 1
    """
    # Validate size
    if not isinstance(size, int) or size < 1:
        raise ValueError("size must be an integer >= 1")
    
    # Create an iterator from the iterable
    iterator = iter(iterable)
    
    # Yield chunks until the iterator is exhausted
    while True:
        chunk = []
        for _ in range(size):
            try:
                chunk.append(next(iterator))
            except StopIteration:
                # If we have a partial chunk, yield it before stopping
                if chunk:
                    yield chunk
                return
        
        # Yield the full chunk
        yield chunk
