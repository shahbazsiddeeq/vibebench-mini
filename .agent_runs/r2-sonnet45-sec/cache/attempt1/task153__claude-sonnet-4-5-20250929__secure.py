import hashlib
import os
from pathlib import Path


def checksum_manifest(root: str) -> dict[str, str]:
    """
    Walk the directory tree rooted at `root` and return a manifest mapping
    each regular file's path (relative to `root`) to its SHA-256 digest.
    
    Args:
        root: Root directory path to scan
        
    Returns:
        Dictionary mapping relative file paths to lowercase hex SHA-256 digests,
        sorted by key ascending. Paths use POSIX '/' separators.
        
    Raises:
        FileNotFoundError: If root does not exist
        NotADirectoryError: If root exists but is not a directory
    """
    # Validate root exists
    root_path = Path(root)
    if not root_path.exists():
        raise FileNotFoundError(f"Root directory does not exist: {root}")
    
    # Validate root is a directory
    if not root_path.is_dir():
        raise NotADirectoryError(f"Root is not a directory: {root}")
    
    manifest = {}
    
    # Walk the directory tree
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            # Get full path to file
            file_path = os.path.join(dirpath, filename)
            
            # Calculate relative path from root
            rel_path = os.path.relpath(file_path, root)
            
            # Normalize path separators to POSIX '/'
            posix_path = rel_path.replace(os.sep, '/')
            
            # Calculate SHA-256 hash by streaming chunks
            sha256_hash = hashlib.sha256()
            try:
                with open(file_path, 'rb') as f:
                    # Read in chunks to handle large files
                    while True:
                        chunk = f.read(65536)  # 64KB chunks
                        if not chunk:
                            break
                        sha256_hash.update(chunk)
                
                # Store lowercase hex digest
                manifest[posix_path] = sha256_hash.hexdigest().lower()
            except (OSError, IOError):
                # Skip files that can't be read (permissions, etc.)
                # This is a security-conscious approach to avoid exposing internals
                continue
    
    # Return sorted dictionary by keys
    return dict(sorted(manifest.items()))
