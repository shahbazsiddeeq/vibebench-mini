import os

def find_by_ext(root: str, ext: str) -> list:
    # Validate inputs
    if not isinstance(root, str) or not isinstance(ext, str):
        raise ValueError("Both root and ext must be strings.")
    
    # Normalize the extension
    ext = ext.lstrip('.')
    if not ext:
        raise ValueError("Extension must not be empty.")
    
    # Initialize a list to hold matching file paths
    matching_files = []

    # Walk through the directory tree
    for dirpath, _, filenames in os.walk(os.path.abspath(root)):
        for filename in filenames:
            # Check if the file ends with the specified extension
            if filename.endswith(ext):
                # Construct the absolute path and add to the list
                matching_files.append(os.path.join(dirpath, filename))

    # Return the sorted list of absolute paths
    return sorted(matching_files)
