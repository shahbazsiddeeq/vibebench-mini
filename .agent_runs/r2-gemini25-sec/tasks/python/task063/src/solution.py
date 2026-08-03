import hashlib
import os

def sha256_file(path: str) -> str:
    """
    Calculates the SHA-256 hash of a file's contents.

    Args:
        path: The path to the file.

    Returns:
        The hexadecimal SHA-256 digest of the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        TypeError: If the path is not a string.
        ValueError: If the path is empty.
        OSError: For other OS-related errors during file operations.
    """
    if not isinstance(path, str):
        raise TypeError("File path must be a string.")
    if not path:
        raise ValueError("File path cannot be empty.")

    # Normalize the path to prevent directory traversal issues, though
    # os.path.abspath is more for canonical representation than security
    # against malicious paths in this specific context (hashlib reads content).
    # The primary security concern here is ensuring the path points to an
    # existing, readable file and handling errors gracefully.
    # os.path.abspath(path)

    # Check if the file exists before attempting to open it.
    # This helps provide a more specific error message (FileNotFoundError)
    # rather than a generic OSError from open().
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file or directory: '{path}'")

    # Further check if it's actually a file and not a directory or other special file.
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Path is not a file: '{path}'")

    hasher = hashlib.sha256()
    try:
        # Open the file in binary read mode.
        # Using a 'with' statement ensures the file is properly closed.
        with open(path, 'rb') as f:
            # Read the file in chunks to handle large files efficiently
            # and avoid loading the entire file into memory.
            # A buffer size of 4096 bytes (4KB) is a common and reasonable choice.
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
    except PermissionError:
        raise PermissionError(f"Permission denied to read file: '{path}'")
    except OSError as e:
        # Catch other potential OS errors during file reading
        raise OSError(f"Error reading file '{path}': {e}") from e

    return hasher.hexdigest()
