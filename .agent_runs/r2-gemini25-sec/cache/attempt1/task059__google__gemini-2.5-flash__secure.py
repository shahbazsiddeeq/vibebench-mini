import os

def tail(path: str, n: int) -> list[str]:
    """
    Returns the last n lines of a file as a list (without newlines).

    Args:
        path: The path to the file.
        n: The number of lines to retrieve.

    Returns:
        A list of strings, where each string is a line from the end of the file.

    Raises:
        ValueError: If n is less than 0.
        FileNotFoundError: If the file does not exist.
        IOError: If there is an error reading the file.
    """
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n cannot be negative")

    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file or directory: '{path}'")
    if not os.path.isfile(path):
        raise IOError(f"Path is not a file: '{path}'")

    # Using a deque or a list with append/pop(0) would be more memory efficient
    # for very large files if we only needed a fixed number of lines,
    # but for simplicity and given the constraints, reading all lines
    # and then slicing is acceptable for typical use cases.
    # For extremely large files where reading all into memory is an issue,
    # a more advanced approach involving seeking from the end would be needed.
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            lines = [line.rstrip('\n') for line in f]
        return lines[-n:]
    except OSError as e:
        # Catching more general OSError for other potential file system errors
        raise IOError(f"Error reading file '{path}': {e}") from e
