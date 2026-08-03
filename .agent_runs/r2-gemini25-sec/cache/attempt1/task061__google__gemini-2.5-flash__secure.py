import os

def dir_size(path: str) -> int:
    """
    Calculates the total size in bytes of all regular files under `path`,
    searched recursively.

    Args:
        path: The path to the directory.

    Returns:
        The total size in bytes of all regular files.

    Raises:
        FileNotFoundError: If `path` does not exist.
        NotADirectoryError: If `path` exists but is not a directory.
    """
    if not isinstance(path, str):
        raise TypeError("Path must be a string.")

    # Sanitize path to prevent directory traversal issues
    # This is a basic sanitization; for more complex scenarios,
    # consider `os.path.abspath` and further validation.
    # However, for this specific problem, `os.path.exists` and `os.path.isdir`
    # will handle most immediate security concerns related to path validity.
    # We'll use the provided path directly as `os.path` functions are robust.

    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file or directory: '{path}'")

    if not os.path.isdir(path):
        raise NotADirectoryError(f"Not a directory: '{path}'")

    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                filepath = os.path.join(dirpath, f)
                # Check if it's a regular file and not a symbolic link
                # os.path.isfile() returns true for regular files and symlinks to regular files.
                # os.path.islink() checks if the path itself is a symlink.
                # We want to count only "real" regular files, not symlinks.
                if os.path.isfile(filepath) and not os.path.islink(filepath):
                    try:
                        total_size += os.path.getsize(filepath)
                    except OSError as e:
                        # Handle cases where file might be inaccessible or disappear during walk
                        # Log the error if necessary, but don't expose internal details.
                        # For this problem, we'll silently skip inaccessible files.
                        pass
    except OSError as e:
        # Catch potential OS errors during directory traversal (e.g., permission denied)
        # Re-raise as a generic OSError or a more specific custom error if needed.
        # For this problem, we'll let the original OSError propagate if it's critical,
        # or wrap it if we want to hide internal details.
        # A simple re-raise is acceptable here as it's an external system error.
        raise OSError(f"Error accessing directory '{path}': {e}") from e

    return total_size
