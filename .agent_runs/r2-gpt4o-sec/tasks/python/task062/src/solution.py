import os
import hashlib
from collections import defaultdict

def find_duplicates(root):
    if not isinstance(root, str):
        raise ValueError("The root path must be a string.")
    
    duplicates = defaultdict(list)

    try:
        for dirpath, _, filenames in os.walk(root):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if os.path.isfile(file_path):
                    try:
                        file_hash = sha256_file(file_path)
                        duplicates[file_hash].append(file_path)
                    except (OSError, IOError):
                        continue
    except Exception as e:
        raise RuntimeError("An error occurred while scanning the directory.") from e

    # Filter out entries with less than 2 files
    return {hash: paths for hash, paths in duplicates.items() if len(paths) > 1}

def sha256_file(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
    except (OSError, IOError) as e:
        raise RuntimeError(f"Failed to read file: {file_path}") from e
    return sha256.hexdigest()
