import os
from pathlib import Path


def find_by_ext(root, ext):
    """
    Recursively finds all regular files under `root` whose name ends
    with the given extension and returns a sorted list of absolute paths.
    
    Args:
        root: The root directory to search in (can be relative or absolute)
        ext: The file extension to match (with or without leading dot)
    
    Returns:
        A sorted list of absolute paths to matching files
    """
    # Normalize the extension to ensure it starts with a dot
    if not ext.startswith('.'):
        ext = '.' + ext
    
    # Convert root to an absolute path
    root_path = Path(root).resolve()
    
    # Collect matching files
    matching_files = []
    
    # Walk through the directory tree
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            # Check if the file ends with the extension
            if filename.endswith(ext):
                # Get the absolute path
                file_path = os.path.join(dirpath, filename)
                matching_files.append(file_path)
    
    # Sort and return
    return sorted(matching_files)
