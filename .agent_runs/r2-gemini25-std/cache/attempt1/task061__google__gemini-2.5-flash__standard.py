import os


def dir_size(path):
    """
    Calculates the total size in bytes of all regular files under `path`,
    searched recursively.

    Args:
        path (str): The path to the directory.

    Returns:
        int: The total size in bytes.

    Raises:
        FileNotFoundError: If `path` does not exist.
        NotADirectoryError: If `path` exists but is not a directory.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file or directory: '{path}'")
    if not os.path.isdir(path):
        raise NotADirectoryError(f"Not a directory: '{path}'")

    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            filepath = os.path.join(dirpath, f)
            # Check if it's a regular file and not a symbolic link
            if os.path.isfile(filepath) and not os.path.islink(filepath):
                total_size += os.path.getsize(filepath)
    return total_size
