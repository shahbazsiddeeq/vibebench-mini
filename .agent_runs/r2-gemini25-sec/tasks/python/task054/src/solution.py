import os

def find_by_ext(root: str, ext: str) -> list[str]:
    """
    Recursively finds all regular files under `root` whose name ends
    with the given extension and returns a sorted list of absolute paths.
    The extension may be supplied with or without a leading dot: both ".py" and "py" match
    files ending in ".py". Matching is on the final suffix only.
    Every returned path is absolute (resolved). The list is sorted in ascending string order.
    If no files match, return an empty list.
    """
    if not isinstance(root, str) or not isinstance(ext, str):
        raise TypeError("Both 'root' and 'ext' must be strings.")

    if not root:
        return []

    # Sanitize and normalize the extension
    ext = ext.strip()
    if not ext:
        return []
    if ext.startswith('.'):
        normalized_ext = ext
    else:
        normalized_ext = '.' + ext

    # Resolve the root path immediately to handle relative paths correctly
    try:
        resolved_root = os.path.abspath(root)
        if not os.path.exists(resolved_root):
            return []
        if not os.path.isdir(resolved_root):
            # If root is a file, check if it matches the extension
            if os.path.isfile(resolved_root) and resolved_root.endswith(normalized_ext):
                return [resolved_root]
            return []
    except OSError:
        # Handle cases where path might be invalid or inaccessible
        return []

    found_files = []
    try:
        for dirpath, _, filenames in os.walk(resolved_root):
            for filename in filenames:
                if filename.endswith(normalized_ext):
                    full_path = os.path.join(dirpath, filename)
                    # Resolve to absolute path to ensure consistency, though os.walk already gives absolute from resolved_root
                    # os.path.abspath is sufficient here as os.walk already builds absolute paths from resolved_root
                    # For robustness, we can call resolve() but abspath is usually enough for os.walk results
                    found_files.append(os.path.abspath(full_path))
    except OSError:
        # Handle cases where directories might become inaccessible during walk
        pass

    found_files.sort()
    return found_files
