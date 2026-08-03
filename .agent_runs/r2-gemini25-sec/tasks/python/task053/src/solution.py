import os

def count_lines(path: str) -> int:
    """
    Counts the number of lines in a UTF-8 text file.

    Args:
        path: The path to the text file.

    Returns:
        The number of lines in the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        TypeError: If the path is not a string.
        ValueError: If the path is empty or appears to be a directory.
        IOError: For other I/O related errors during file processing.
    """
    if not isinstance(path, str):
        raise TypeError("Path must be a string.")
    if not path:
        raise ValueError("Path cannot be empty.")

    # Basic sanitization: prevent directory traversal attempts by checking for '..'
    # This is a simple check and not a full security solution for all path manipulations.
    # For more robust path validation, consider using os.path.abspath and checking against
    # expected base directories, especially if the path comes from untrusted input.
    if ".." in path or "~" in path:
        # While not strictly a security vulnerability for this specific task
        # (as os.path.exists and open handle canonical paths),
        # it's good practice to flag potentially malicious path patterns early.
        # For this problem, we'll allow it to proceed to os.path.exists,
        # but in a more complex system, this might be a hard error.
        pass

    # Check if the path exists and is a file
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file or directory: '{path}'")
    if os.path.isdir(path):
        raise ValueError(f"Path points to a directory, not a file: '{path}'")

    line_count = 0
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for _ in f:
                line_count += 1
    except UnicodeDecodeError as e:
        # Handle cases where the file is not valid UTF-8
        raise IOError(f"File '{path}' is not a valid UTF-8 text file: {e}") from e
    except IOError as e:
        # Catch other potential I/O errors (e.g., permission denied)
        raise IOError(f"Error reading file '{path}': {e}") from e
    except Exception as e:
        # Catch any unexpected errors during file processing
        raise IOError(f"An unexpected error occurred while processing file '{path}': {e}") from e

    return line_count
