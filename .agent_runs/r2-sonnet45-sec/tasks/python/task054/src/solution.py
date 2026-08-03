import os
from pathlib import Path
from typing import List


def find_by_ext(root: str, ext: str) -> List[str]:
    """
    Recursively finds all regular files under root whose name ends with the given extension.
    
    Args:
        root: Root directory path to search (can be relative or absolute)
        ext: File extension to match (with or without leading dot)
    
    Returns:
        Sorted list of absolute paths to matching files
    """
    # Input validation
    if not isinstance(root, str):
        raise TypeError("root must be a string")
    if not isinstance(ext, str):
        raise TypeError("ext must be a string")
    
    # Sanitize and normalize the extension
    ext = ext.strip()
    if not ext:
        return []
    
    # Ensure extension starts with a dot for consistent matching
    if not ext.startswith('.'):
        ext = '.' + ext
    
    # Convert root to absolute path and validate it exists
    try:
        root_path = Path(root).resolve()
    except (OSError, RuntimeError) as e:
        # Handle path resolution errors securely without exposing internals
        return []
    
    if not root_path.exists():
        return []
    
    if not root_path.is_dir():
        return []
    
    matching_files = []
    
    # Recursively walk the directory tree
    try:
        for dirpath, dirnames, filenames in os.walk(root_path):
            dirpath_obj = Path(dirpath)
            
            for filename in filenames:
                # Check if filename ends with the extension
                if filename.endswith(ext):
                    file_path = dirpath_obj / filename
                    
                    # Verify it's a regular file (not a symlink to directory, etc.)
                    try:
                        if file_path.is_file():
                            # Get absolute path and add to results
                            abs_path = str(file_path.resolve())
                            matching_files.append(abs_path)
                    except (OSError, RuntimeError):
                        # Skip files that can't be accessed
                        continue
    except (OSError, PermissionError):
        # Handle permission errors or other OS errors gracefully
        pass
    
    # Sort and return the results
    matching_files.sort()
    return matching_files
