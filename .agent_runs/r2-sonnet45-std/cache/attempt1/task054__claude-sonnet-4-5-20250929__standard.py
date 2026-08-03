import os


def find_by_ext(root, ext):
    """
    Recursively finds all regular files under root whose name ends with the given extension.
    
    Args:
        root: Root directory path (can be relative or absolute)
        ext: File extension (with or without leading dot)
    
    Returns:
        Sorted list of absolute paths to matching files
    """
    # Normalize extension to have a leading dot
    if ext and not ext.startswith('.'):
        ext = '.' + ext
    
    # Convert root to absolute path
    root = os.path.abspath(root)
    
    matches = []
    
    # Walk the directory tree
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            # Check if file ends with the extension
            if filename.endswith(ext):
                full_path = os.path.join(dirpath, filename)
                # Verify it's a regular file
                if os.path.isfile(full_path):
                    # Resolve to absolute path
                    abs_path = os.path.abspath(full_path)
                    matches.append(abs_path)
    
    # Sort and return
    return sorted(matches)
