import os

def dir_size(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"The path {path} does not exist.")
    if not os.path.isdir(path):
        raise NotADirectoryError(f"The path {path} is not a directory.")
    
    total_size = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if not os.path.islink(file_path):
                total_size += os.path.getsize(file_path)
    
    return total_size
