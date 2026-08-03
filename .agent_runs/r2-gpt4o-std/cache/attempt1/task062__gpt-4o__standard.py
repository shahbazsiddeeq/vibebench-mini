import os
import hashlib
from collections import defaultdict

def find_duplicates(root):
    hash_to_paths = defaultdict(list)

    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            with open(file_path, 'rb') as f:
                file_content = f.read()
                file_hash = hashlib.sha256(file_content).hexdigest()
                hash_to_paths[file_hash].append(file_path)

    # Filter out entries with less than 2 files
    return {h: paths for h, paths in hash_to_paths.items() if len(paths) > 1}
