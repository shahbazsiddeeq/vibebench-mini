import os

def dir_size(path: str) -> int:
    if not os.path.exists(path):
        raise FileNotFoundError(f"The path '{path}' does not exist.")
    
    if not os.path.isdir(path):
        raise NotADirectoryError(f"The path '{path}' is not a directory.")
    
    total_size = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.islink(file_path):
                continue
            try:
                total_size += os.path.getsize(file_path)
            except OSError:
                # Skip files that can't be accessed
                continue
    
    return total_size
