import os
import hashlib
import collections

def find_duplicates(root: str) -> dict[str, list[str]]:
    """
    Finds duplicate files within a given root directory based on their SHA-256 hash.

    Args:
        root: The path to the root directory to search.

    Returns:
        A dictionary where keys are SHA-256 hex hashes and values are lists of
        paths to files that have identical content. Only groups with 2 or more
        files are included.
    """
    if not isinstance(root, str):
        raise TypeError("Root path must be a string.")
    if not os.path.isdir(root):
        # If the root is not a directory, there are no files to process.
        # This also handles cases where the path doesn't exist.
        return {}

    hash_to_paths = collections.defaultdict(list)
    buffer_size = 65536  # 64 KB buffer for reading files

    try:
        for dirpath, _, filenames in os.walk(root):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                # Ensure the path is normalized and absolute for consistent keys
                # and to prevent issues with relative paths or symlinks pointing outside.
                # However, os.walk already provides absolute-like paths relative to root.
                # For security, we should resolve symlinks if we were to modify files,
                # but for just reading, the path provided by os.walk is usually sufficient.
                # We'll use realpath to be safe and consistent.
                try:
                    resolved_file_path = os.path.realpath(file_path)
                    if not os.path.isfile(resolved_file_path):
                        # Skip if it's not a regular file (e.g., broken symlink, directory)
                        continue

                    hasher = hashlib.sha256()
                    with open(resolved_file_path, 'rb') as f:
                        while True:
                            chunk = f.read(buffer_size)
                            if not chunk:
                                break
                            hasher.update(chunk)
                    hash_to_paths[hasher.hexdigest()].append(resolved_file_path)
                except OSError:
                    # Handle cases like permission errors or file disappearing during walk
                    # Log the error if logging was allowed, but for now, just skip the file.
                    continue
                except Exception:
                    # Catch any other unexpected errors during file processing
                    continue
    except OSError:
        # Handle cases where os.walk itself encounters issues (e.g., permission denied on root)
        return {}

    # Filter out groups with only one file
    duplicates = {
        file_hash: paths
        for file_hash, paths in hash_to_paths.items()
        if len(paths) >= 2
    }

    return duplicates
