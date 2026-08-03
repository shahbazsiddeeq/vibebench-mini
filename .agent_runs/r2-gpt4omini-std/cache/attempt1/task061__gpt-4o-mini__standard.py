import os

def dir_size(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"The path '{path}' does not exist.")
    if not os.path.isdir(path):
        raise NotADirectoryError(f"The path '{path}' is not a directory.")
    
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path):  # Only count regular files
                total_size += os.path.getsize(file_path)
    
    return total_size
