import os

def find_by_ext(root, ext):
    """
    Recursively finds all regular files under `root` whose name ends
    with the given extension and returns a sorted list of absolute paths.
    The extension may be supplied with or without a leading dot: both ".py" and "py" match
    files ending in ".py". Matching is on the final suffix only.
    Every returned path is absolute (resolved). The list is sorted in ascending string order.
    If no files match, return an empty list.
    """
    if not os.path.isdir(root):
        return []

    # Ensure the extension starts with a dot for consistent comparison
    if not ext.startswith('.'):
        ext = '.' + ext

    matching_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(ext):
                full_path = os.path.join(dirpath, filename)
                matching_files.append(os.path.abspath(full_path))

    matching_files.sort()
    return matching_files
