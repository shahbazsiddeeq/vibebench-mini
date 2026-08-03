import collections.abc

def chunked(iterable, size):
    """
    Yields successive chunks of up to size elements as lists.

    Args:
        iterable: The input iterable to be chunked.
        size: The maximum size of each chunk. Must be a positive integer.

    Yields:
        A list containing elements of the current chunk.

    Raises:
        ValueError: If size is less than 1.
        TypeError: If size is not an integer.
    """
    if not isinstance(size, int):
        raise TypeError("Chunk size must be an integer.")
    if size < 1:
        raise ValueError("Chunk size must be at least 1.")

    # Ensure iterable is actually iterable
    if not isinstance(iterable, collections.abc.Iterable):
        raise TypeError("Input must be an iterable.")

    iterator = iter(iterable)
    while True:
        chunk = []
        try:
            for _ in range(size):
                chunk.append(next(iterator))
            yield chunk
        except StopIteration:
            if chunk:  # Yield any remaining elements
                yield chunk
            break
