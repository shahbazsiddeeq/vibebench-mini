import os
import hashlib

def find_duplicates(root: str) -> dict[str, list[str]]:
    """
    Finds duplicate files within a given root directory based on their SHA-256 hash.

    Args:
        root: The root directory to search for duplicate files.

    Returns:
        A dictionary where keys are SHA-256 hex hashes and values are lists of
        paths to files with identical content. Only groups with 2 or more files
        are included.
    """
    hash_to_paths = {}

    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, "rb") as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                
                if file_hash not in hash_to_paths:
                    hash_to_paths[file_hash] = []
                hash_to_paths[file_hash].append(filepath)
            except IOError:
                # Skip files that cannot be read (e.g., permission issues)
                continue

    # Filter out groups with less than 2 files
    duplicates = {
        file_hash: paths
        for file_hash, paths in hash_to_paths.items()
        if len(paths) >= 2
    }

    return duplicates
