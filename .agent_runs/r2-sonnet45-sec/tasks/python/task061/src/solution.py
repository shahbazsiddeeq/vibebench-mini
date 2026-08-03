import os
from pathlib import Path


def dir_size(path: str) -> int:
    """
    Calculate the total size in bytes of all regular files under the given path,
    searched recursively.
    
    Args:
        path: Path to the directory to analyze
        
    Returns:
        Total size in bytes of all regular files (excluding symlinks)
        
    Raises:
        FileNotFoundError: If the path does not exist
        NotADirectoryError: If the path exists but is not a directory
    """
    # Validate input type
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    
    # Convert to Path object for safer path handling
    path_obj = Path(path)
    
    # Check if path exists
    if not path_obj.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")
    
    # Check if path is a directory
    if not path_obj.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {path}")
    
    total_size = 0
    
    # Walk through directory tree
    try:
        for entry in path_obj.rglob("*"):
            # Only count regular files, not symlinks or directories
            if entry.is_file() and not entry.is_symlink():
                try:
                    # Get file size safely
                    total_size += entry.stat().st_size
                except (OSError, PermissionError):
                    # Skip files we can't access
                    continue
    except (OSError, PermissionError):
        # If we can't traverse the directory, return what we have so far
        pass
    
    return total_size
