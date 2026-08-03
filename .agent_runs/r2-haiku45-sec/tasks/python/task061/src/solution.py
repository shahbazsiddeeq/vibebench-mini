import os
from pathlib import Path


def dir_size(path: str) -> int:
    """
    Calculate the total size in bytes of all regular files under `path`,
    searched recursively.
    
    Args:
        path: A string representing the directory path to analyze.
    
    Returns:
        The total size in bytes of all regular files under the directory.
        Returns 0 for an empty directory.
    
    Raises:
        FileNotFoundError: If `path` does not exist.
        NotADirectoryError: If `path` exists but is not a directory.
    """
    # Validate input type
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    
    # Convert to Path object for safer operations
    try:
        p = Path(path)
    except (TypeError, ValueError) as e:
        raise FileNotFoundError(f"Invalid path: {path}") from e
    
    # Check if path exists
    if not p.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")
    
    # Check if path is a directory
    if not p.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {path}")
    
    total_size = 0
    
    # Walk through the directory tree
    for root, dirs, files in os.walk(p):
        for filename in files:
            filepath = os.path.join(root, filename)
            
            # Only count regular files, not symlinks
            # Use lstat to not follow symlinks
            try:
                stat_info = os.lstat(filepath)
                # Check if it's a regular file (not a symlink, directory, etc.)
                if os.path.isfile(filepath) and not os.path.islink(filepath):
                    total_size += stat_info.st_size
            except (OSError, IOError):
                # Skip files that cannot be accessed
                continue
    
    return total_size
