import os

def tail(path: str, n: int) -> list[str]:
    """
    Returns the last n lines of a file as a list (without newlines).
    If n > file length, all lines are returned.

    Args:
        path: The path to the file.
        n: The number of lines to retrieve from the end of the file.

    Returns:
        A list of strings, where each string is a line from the file
        (without the trailing newline character).

    Raises:
        ValueError: If n is less than 0.
        FileNotFoundError: If the file specified by path does not exist.
        IOError: If an I/O error occurs during file operations.
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

    if n == 0:
        return []

    try:
        with open(path, 'r', encoding='utf-8') as f:
            # Read all lines into a list
            lines = f.readlines()

        # Strip newline characters from each line
        stripped_lines = [line.rstrip('\n') for line in lines]

        # Return the last n lines
        return stripped_lines[-n:]
    except OSError as e:
        # Catch potential OS errors like permission denied
        raise IOError(f"Error accessing file '{path}': {e}") from e
    except Exception as e:
        # Catch any other unexpected errors during file processing
        raise IOError(f"An unexpected error occurred while reading '{path}': {e}") from e
