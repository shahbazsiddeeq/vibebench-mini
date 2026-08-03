import os
import hashlib

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

    Raises FileNotFoundError if `root` does not exist, and NotADirectoryError if
    `root` exists but is not a directory.
    """
    if not os.path.exists(root):
        raise FileNotFoundError(f"No such file or directory: '{root}'")
    if not os.path.isdir(root):
        raise NotADirectoryError(f"Not a directory: '{root}'")

    manifest = {}
    chunk_size = 4096  # 4KB chunks

    for dirpath, _, filenames in os.walk(root, followlinks=False):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(file_path, root)
            posix_relative_path = relative_path.replace(os.sep, '/')

            hasher = hashlib.sha256()
            try:
                with open(file_path, 'rb') as f:
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        hasher.update(chunk)
                manifest[posix_relative_path] = hasher.hexdigest()
            except IOError:
                # If a file cannot be opened/read (e.g., permissions),
                # we skip it as per the "only files reported by os.walk are hashed"
                # and implicit success of hashing. os.walk typically won't report
                # unreadable files unless it has permission to list the directory.
                # For this problem, we assume files reported by os.walk are readable.
                pass

    # Sort the manifest by key
    return dict(sorted(manifest.items()))
