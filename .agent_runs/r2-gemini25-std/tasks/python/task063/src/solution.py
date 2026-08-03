import hashlib
import os

def sha256_file(path: str) -> str:
    """
    Calculates the SHA-256 hash of a file's contents.

    Args:
        path: The path to the file.

    Returns:
        The hexadecimal SHA-256 digest of the file's contents.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file or directory: '{path}'")

    hasher = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            while chunk := f.read(4096):  # Read in chunks to handle large files
                hasher.update(chunk)
    except IOError as e:
        # Re-raise as FileNotFoundError if the file was deleted between exists check and open
        # or if there's another I/O error that prevents reading.
        # For simplicity and given the test cases, we assume FileNotFoundError is the primary
        # error to catch for non-existence. Other I/O errors might be propagated.
        if not os.path.exists(path): # Double check if file disappeared
            raise FileNotFoundError(f"No such file or directory: '{path}'") from e
        raise # Re-raise other IOError

    return hasher.hexdigest()
