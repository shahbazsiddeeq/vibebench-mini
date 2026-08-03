import os
from pathlib import Path


def dir_size(path: str) -> int:
    """
    Calculate the total size in bytes of all regular files under `path`,
    searched recursively. Symbolic links are not followed or counted.
    
    Args:
        path: The directory path to calculate size for
        
    Returns:
        Total size in bytes of all regular files
        
    Raises:
        FileNotFoundError: if path does not exist
        NotADirectoryError: if path exists but is not a directory
    """
    path_obj = Path(path)
    
    # Check if path exists
    if not path_obj.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")
    
    # Check if path is a directory
    if not path_obj.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {path}")
    
    total_size = 0
    
    # Walk through directory recursively
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            # Only count regular files, not symlinks
            if os.path.isfile(file_path) and not os.path.islink(file_path):
                total_size += os.path.getsize(file_path)
    
    return total_size
