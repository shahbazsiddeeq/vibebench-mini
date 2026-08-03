import os


def dir_size(path):
    """
    Returns the total size in bytes of all regular files under `path`,
    searched recursively.
    
    Args:
        path: Directory path to calculate size for
        
    Returns:
        Total size in bytes of all regular files
        
    Raises:
        FileNotFoundError: if path does not exist
        NotADirectoryError: if path exists but is not a directory
    """
    # Check if path exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path does not exist: {path}")
    
    # Check if path is a directory
    if not os.path.isdir(path):
        raise NotADirectoryError(f"Path is not a directory: {path}")
    
    total_size = 0
    
    # Walk through directory tree
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            
            # Only count regular files, not symlinks
            if os.path.isfile(filepath) and not os.path.islink(filepath):
                total_size += os.path.getsize(filepath)
    
    return total_size
