import hashlib
import os


def checksum_manifest(root: str) -> dict[str, str]:
    """
    Walk the directory tree rooted at `root` and return a manifest mapping
    each regular file's path (relative to `root`) to the lowercase hex SHA-256
    digest of that file's raw bytes.
    
    Keys use POSIX '/' separators regardless of platform, and the returned
    dict is ordered by key ascending (sorted).
    
    Raises FileNotFoundError if `root` does not exist, and NotADirectoryError
    if `root` exists but is not a directory.
    """
    # Check if root exists
    if not os.path.exists(root):
        raise FileNotFoundError(f"No such file or directory: '{root}'")
    
    # Check if root is a directory
    if not os.path.isdir(root):
        raise NotADirectoryError(f"Not a directory: '{root}'")
    
    manifest = {}
    
    # Walk the directory tree
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            
            # Calculate relative path from root
            relpath = os.path.relpath(filepath, root)
            
            # Convert to POSIX path (replace os.sep with '/')
            posix_relpath = relpath.replace(os.sep, '/')
            
            # Calculate SHA-256 hash by streaming chunks
            sha256_hash = hashlib.sha256()
            with open(filepath, 'rb') as f:
                while True:
                    chunk = f.read(8192)  # Read in 8KB chunks
                    if not chunk:
                        break
                    sha256_hash.update(chunk)
            
            # Store the lowercase hex digest
            manifest[posix_relpath] = sha256_hash.hexdigest()
    
    # Return sorted by key
    return dict(sorted(manifest.items()))
