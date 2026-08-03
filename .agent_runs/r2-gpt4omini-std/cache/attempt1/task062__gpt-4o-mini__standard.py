import os
import hashlib
from collections import defaultdict

def find_duplicates(root):
    file_hashes = defaultdict(list)

    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'rb') as f:
                    file_content = f.read()
                    file_hash = hashlib.sha256(file_content).hexdigest()
                    file_hashes[file_hash].append(filepath)

    # Filter out groups with less than 2 files
    return {hash_key: paths for hash_key, paths in file_hashes.items() if len(paths) > 1}
