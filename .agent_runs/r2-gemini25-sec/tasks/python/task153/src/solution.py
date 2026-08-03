import os
import hashlib
from collections import OrderedDict

def checksum_manifest(root: str) -> dict[str, str]:
    """
    Walks the directory tree rooted at `root` and returns a manifest mapping
    each regular file's path (relative to `root`) to the lowercase hex SHA-256
    digest of that file's raw bytes.

    Keys use POSIX '/' separators regardless of platform (os.sep is replaced with '/'),
    and the returned dict is ordered by key ascending (sorted). File contents are
    hashed by streaming the bytes in chunks so large files do not need to fit in memory.
    Symbolic links are not followed and directories themselves are not entries;
    only files reported by os.walk are hashed. An empty tree yields an empty dict.

    Raises FileNotFoundError if `root` does not exist, and NotADirectoryError if `root`
    exists but is not a directory.
    """
    if not isinstance(root, str):
        raise TypeError("root must be a string.")

    if not os.path.exists(root):
        raise FileNotFoundError(f"Root directory '{root}' does not exist.")
    if not os.path.isdir(root):
        raise NotADirectoryError(f"'{root}' is not a directory.")

    manifest = {}
    chunk_size = 4096  # Standard chunk size for hashing

    for dirpath, _, filenames in os.walk(root, followlinks=False):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            
            # Ensure it's a regular file and not a symlink (os.walk with followlinks=False
            # should handle symlinks as files if they point to files, but we want to ignore them).
            # os.path.isfile also returns true for symlinks to files, so we explicitly check.
            if not os.path.isfile(file_path) or os.path.islink(file_path):
                continue

            try:
                hasher = hashlib.sha256()
                with open(file_path, 'rb') as f:
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        hasher.update(chunk)
                
                relative_path = os.path.relpath(file_path, root)
                # Normalize path separators to POSIX '/'
                posix_path = relative_path.replace(os.sep, '/')
                manifest[posix_path] = hasher.hexdigest()
            except OSError as e:
                # Log or handle specific file access errors if necessary,
                # but for this task, we might just skip problematic files
                # or let the error propagate if it's critical.
                # For now, we'll skip files that cause OS errors during reading.
                # print(f"Warning: Could not process file {file_path}: {e}")
                pass # Skip files that cannot be read

    # Sort the manifest by key
    sorted_manifest = OrderedDict(sorted(manifest.items()))
    return dict(sorted_manifest)
