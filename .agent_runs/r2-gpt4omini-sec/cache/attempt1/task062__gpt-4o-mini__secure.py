import os
import hashlib
from collections import defaultdict

def find_duplicates(root: str) -> dict:
    if not os.path.isdir(root):
        raise ValueError("The provided path is not a valid directory.")
    
    file_hashes = defaultdict(list)

    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'rb') as file:
                        file_content = file.read()
                        file_hash = hashlib.sha256(file_content).hexdigest()
                        file_hashes[file_hash].append(file_path)
                except (OSError, IOError):
                    continue  # Skip files that cannot be read

    # Filter out hashes with less than 2 files
    duplicates = {file_hash: paths for file_hash, paths in file_hashes.items() if len(paths) > 1}

    return duplicates
