import os
import hashlib

def dir_hash(path):
    """
    Returns a deterministic SHA-256 hex digest over the contents of a directory tree.

    Recursively collects every regular file under path, ignores directories themselves,
    and sorts the files by their relative POSIX path (relative to path).
    For each file, feeds into a single SHA-256 hash, in order, the byte length of the
    UTF-8 relative path followed by a colon, then the path bytes, then the byte length
    of the file content followed by a colon, then the content bytes.
    Returns the hexdigest. The length-delimited framing guarantees two different trees
    cannot produce the same digest by shifting a path/content boundary.
    Raises ValueError if path is not a directory.
    The result is stable across runs and independent of filesystem iteration order.
    """
    if not os.path.isdir(path):
        raise ValueError(f"Path '{path}' is not a directory.")

    hasher = hashlib.sha256()
    base_path = os.path.abspath(path)
    
    file_data = []

    for root, _, files in os.walk(base_path):
        for file_name in files:
            full_path = os.path.join(root, file_name)
            
            # Ensure relative path is POSIX-style and relative to the base_path
            relative_path = os.path.relpath(full_path, base_path).replace(os.sep, '/')
            
            file_data.append((relative_path, full_path))

    # Sort files by their relative POSIX path
    file_data.sort(key=lambda x: x[0])

    for relative_path, full_path in file_data:
        relative_path_bytes = relative_path.encode('utf-8')
        
        hasher.update(str(len(relative_path_bytes)).encode('utf-8'))
        hasher.update(b':')
        hasher.update(relative_path_bytes)
        
        with open(full_path, 'rb') as f:
            content_bytes = f.read()
        
        hasher.update(str(len(content_bytes)).encode('utf-8'))
        hasher.update(b':')
        hasher.update(content_bytes)

    return hasher.hexdigest()
