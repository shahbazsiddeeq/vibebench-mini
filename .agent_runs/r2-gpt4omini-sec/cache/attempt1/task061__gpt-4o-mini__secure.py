# src/solution.py

import os

def dir_size(path: str) -> int:
    # Validate the input path
    if not isinstance(path, str):
        raise ValueError("Path must be a string.")
    
    # Check if the path exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"The path '{path}' does not exist.")
    
    # Check if the path is a directory
    if not os.path.isdir(path):
        raise NotADirectoryError(f"The path '{path}' is not a directory.")
    
    total_size = 0
    
    # Walk through the directory
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            # Only count regular files, not symbolic links
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    
    return total_size
