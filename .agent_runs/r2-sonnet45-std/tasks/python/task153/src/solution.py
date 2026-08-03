import hashlib
import os


def checksum_manifest(root: str) -> dict[str, str]:
    """
    Walk the directory tree rooted at `root` and return a manifest mapping
    each regular file's path (relative to `root`) to its SHA-256 digest.
    
    Args:
        root: Root directory path to scan
        
    Returns:
        Dictionary mapping relative file paths to lowercase hex SHA-256 digests,
        sorted by key ascending. Paths use '/' separators regardless of platform.
        
    Raises:
        FileNotFoundError: If root does not exist
        NotADirectoryError: If root exists but is not a directory
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
            # Get the full path to the file
            filepath = os.path.join(dirpath, filename)
            
            # Skip if it's a symbolic link (only process regular files)
            if os.path.islink(filepath):
                continue
            
            # Calculate relative path from root
            relpath = os.path.relpath(filepath, root)
            
            # Convert to POSIX-style path (replace os.sep with '/')
            posix_path = relpath.replace(os.sep, '/')
            
            # Calculate SHA-256 hash by streaming chunks
            sha256_hash = hashlib.sha256()
            with open(filepath, 'rb') as f:
                # Read in chunks to handle large files
                while True:
                    chunk = f.read(65536)  # 64KB chunks
                    if not chunk:
                        break
                    sha256_hash.update(chunk)
            
            # Store the lowercase hex digest
            manifest[posix_path] = sha256_hash.hexdigest().lower()
    
    # Return sorted by key
    return dict(sorted(manifest.items()))
