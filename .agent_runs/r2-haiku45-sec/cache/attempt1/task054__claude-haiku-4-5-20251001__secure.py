import os
from pathlib import Path


def find_by_ext(root, ext):
    """
    Recursively finds all regular files under `root` whose name ends with the given extension.
    Returns a sorted list of absolute paths.
    
    Args:
        root: The root directory to search (can be relative or absolute)
        ext: The file extension to match (with or without leading dot)
    
    Returns:
        A sorted list of absolute paths to matching files
    """
    # Validate inputs
    if not isinstance(root, (str, bytes, os.PathLike)):
        raise TypeError("root must be a path-like object")
    if not isinstance(ext, str):
        raise TypeError("ext must be a string")
    
    # Normalize the extension - ensure it starts with a dot
    if ext and not ext.startswith('.'):
        ext = '.' + ext
    
    # Convert root to an absolute path
    root_path = Path(root).resolve()
    
    # Validate that root exists and is a directory
    if not root_path.exists():
        raise FileNotFoundError(f"root path does not exist: {root}")
    if not root_path.is_dir():
        raise NotADirectoryError(f"root path is not a directory: {root}")
    
    matching_files = []
    
    # Recursively walk through the directory tree
    try:
        for dirpath, dirnames, filenames in os.walk(root_path):
            for filename in filenames:
                # Check if the filename ends with the extension
                if filename.endswith(ext):
                    # Get the absolute path
                    file_path = Path(dirpath) / filename
                    # Verify it's a regular file (not a symlink to directory, etc.)
                    if file_path.is_file():
                        matching_files.append(str(file_path.resolve()))
    except (OSError, PermissionError):
        # If we encounter permission errors or other OS errors during traversal,
        # return what we've found so far (graceful degradation)
        pass
    
    # Sort and return
    return sorted(matching_files)
