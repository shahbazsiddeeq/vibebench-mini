import os

def tail(path: str, n: int) -> list[str]:
    """
    Returns the last n lines of a file as a list (without newlines).

    Args:
        path: The path to the file.
        n: The number of lines to retrieve from the end of the file.

    Returns:
        A list of strings, where each string is a line from the end of the file.

    Raises:
        ValueError: If n is less than 0.
        FileNotFoundError: If the file specified by path does not exist.
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer.")

    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file or directory: '{path}'")

    if n == 0:
        return []

    with open(path, 'r') as f:
        lines = f.readlines()

    # Remove trailing newlines from each line
    stripped_lines = [line.rstrip('\n') for line in lines]

    return stripped_lines[-n:]
