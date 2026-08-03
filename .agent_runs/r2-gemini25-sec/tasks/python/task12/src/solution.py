import os
import hashlib

def dir_hash(path: str) -> str:
    """
    Calculates a deterministic SHA-256 hex digest over the contents of a directory tree.

    Recursively collects every regular file under path, ignores directories themselves,
    and sorts the files by their relative POSIX path (relative to path). For each file,
    feeds into a single SHA-256 hash, in order, the byte length of the UTF-8 relative
    path followed by a colon, then the path bytes, then the byte length of the file
    content followed by a colon, then the content bytes.

    Args:
        path: The path to the directory.

    Returns:
        The SHA-256 hexdigest of the directory's contents.

    Raises:
        ValueError: If path is not a directory or if there's an issue reading files.
    """
    if not isinstance(path, str):
        raise ValueError("Path must be a string.")

    if not os.path.isdir(path):
        raise ValueError(f"Path '{path}' is not a directory.")

    hasher = hashlib.sha256()
    base_path = os.path.abspath(path)
    
    file_data = []

    try:
        for root, _, files in os.walk(base_path):
            for file_name in files:
                full_path = os.path.join(root, file_name)
                
                # Ensure we only process regular files and handle symlinks carefully
                if not os.path.islink(full_path) and os.path.isfile(full_path):
                    relative_path = os.path.relpath(full_path, base_path)
                    # Normalize path separators to POSIX style for consistency
                    posix_relative_path = relative_path.replace(os.sep, '/')
                    file_data.append((posix_relative_path, full_path))
    except OSError as e:
        raise ValueError(f"Error traversing directory '{path}': {e}")

    # Sort files by their relative POSIX path for deterministic order
    file_data.sort(key=lambda x: x[0])

    for rel_path_str, full_path in file_data:
        try:
            rel_path_bytes = rel_path_str.encode('utf-8')
            hasher.update(str(len(rel_path_bytes)).encode('ascii'))
            hasher.update(b':')
            hasher.update(rel_path_bytes)

            with open(full_path, 'rb') as f:
                content_bytes = f.read()
            
            hasher.update(str(len(content_bytes)).encode('ascii'))
            hasher.update(b':')
            hasher.update(content_bytes)
        except OSError as e:
            raise ValueError(f"Error reading file '{full_path}': {e}")
        except UnicodeEncodeError as e:
            raise ValueError(f"Error encoding path '{rel_path_str}': {e}")

    return hasher.hexdigest()
