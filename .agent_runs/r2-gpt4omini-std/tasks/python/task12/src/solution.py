import os
import hashlib

def dir_hash(path):
    if not os.path.isdir(path):
        raise ValueError(f"{path} is not a directory")

    hash_obj = hashlib.sha256()
    file_paths = []

    # Collect all regular files with their relative paths
    for root, _, files in os.walk(path):
        for file in sorted(files):
            rel_path = os.path.relpath(os.path.join(root, file), path)
            file_paths.append(rel_path)

    # Process each file in sorted order
    for rel_path in file_paths:
        # Get the file content
        with open(os.path.join(path, rel_path), 'rb') as f:
            content = f.read()

        # Prepare the data to hash
        rel_path_bytes = rel_path.encode('utf-8')
        content_length = len(content)
        rel_path_length = len(rel_path_bytes)

        # Update the hash with the length and content
        hash_obj.update(f"{rel_path_length}:".encode('utf-8'))
        hash_obj.update(rel_path_bytes)
        hash_obj.update(f"{content_length}:".encode('utf-8'))
        hash_obj.update(content)

    return hash_obj.hexdigest()
