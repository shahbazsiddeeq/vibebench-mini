import os
import hashlib
import pathlib

def dir_hash(path: str) -> str:
    # Validate the input path
    path_obj = pathlib.Path(path)
    if not path_obj.is_dir():
        raise ValueError("The provided path is not a directory.")

    # Collect all regular files in the directory tree
    file_paths = sorted(path_obj.rglob('*'))  # Use rglob to get all files recursively
    file_entries = []

    for file_path in file_paths:
        if file_path.is_file():
            # Get the relative path
            rel_path = file_path.relative_to(path_obj).as_posix()
            # Read the file content
            with open(file_path, 'rb') as f:
                content = f.read()
            # Prepare the entry for hashing
            file_entries.append((rel_path.encode('utf-8'), content))

    # Create a SHA-256 hash object
    hash_obj = hashlib.sha256()

    # Process each file entry
    for rel_path, content in file_entries:
        # Length of the relative path
        rel_path_length = len(rel_path)
        # Length of the content
        content_length = len(content)

        # Update the hash with the required format
        hash_obj.update(f"{rel_path_length}:".encode('utf-8'))
        hash_obj.update(rel_path)
        hash_obj.update(f"{content_length}:".encode('utf-8'))
        hash_obj.update(content)

    # Return the hex digest of the hash
    return hash_obj.hexdigest()
