import hashlib
import os
from pathlib import Path


def checksum_manifest(root: str) -> dict[str, str]:
    """
    Walk the directory tree rooted at `root` and return a manifest mapping
    each regular file's path (relative to `root`) to the lowercase hex SHA-256
    digest of that file's raw bytes.
    
    Keys use POSIX '/' separators regardless of platform, and the returned
    dict is ordered by key ascending (sorted).
    
    Args:
        root: Path to the root directory to walk
        
    Returns:
        Dictionary mapping relative file paths to SHA-256 digests
        
    Raises:
        FileNotFoundError: If root does not exist
        NotADirectoryError: If root exists but is not a directory
    """
    root_path = Path(root)
    
    # Validate that root exists
    if not root_path.exists():
        raise FileNotFoundError(f"No such file or directory: '{root}'")
    
    # Validate that root is a directory
    if not root_path.is_dir():
        raise NotADirectoryError(f"Not a directory: '{root}'")
    
    manifest = {}
    
    # Walk the directory tree
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            file_path = Path(dirpath) / filename
            
            # Skip symbolic links
            if file_path.is_symlink():
                continue
            
            # Only process regular files
            if not file_path.is_file():
                continue
            
            # Calculate relative path with POSIX separators
            try:
                rel_path = file_path.relative_to(root_path)
            except ValueError:
                # Should not happen, but handle gracefully
                continue
            
            # Convert to POSIX path (forward slashes)
            posix_path = rel_path.as_posix()
            
            # Calculate SHA-256 digest by streaming chunks
            sha256_hash = hashlib.sha256()
            try:
                with open(file_path, 'rb') as f:
                    while True:
                        chunk = f.read(65536)  # 64KB chunks
                        if not chunk:
                            break
                        sha256_hash.update(chunk)
            except (OSError, IOError):
                # Skip files that cannot be read
                continue
            
            # Store the digest in lowercase hex
            manifest[posix_path] = sha256_hash.hexdigest()
    
    # Return sorted by key
    return dict(sorted(manifest.items()))
