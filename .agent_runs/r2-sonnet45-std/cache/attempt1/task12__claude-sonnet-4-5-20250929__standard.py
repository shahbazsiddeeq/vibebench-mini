import hashlib
import os
from pathlib import Path


def dir_hash(path):
    """
    Returns a deterministic SHA-256 hex digest over the contents of a directory tree.
    
    Args:
        path: Path to a directory
        
    Returns:
        SHA-256 hexdigest string
        
    Raises:
        ValueError: If path is not a directory
    """
    path_obj = Path(path)
    
    # Check if path is a directory
    if not path_obj.is_dir():
        raise ValueError(f"Path is not a directory: {path}")
    
    # Collect all regular files recursively
    files = []
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            full_path = Path(root) / filename
            if full_path.is_file():
                # Get relative path from the base path
                rel_path = full_path.relative_to(path_obj)
                files.append(rel_path)
    
    # Sort files by their relative POSIX path
    files.sort(key=lambda p: p.as_posix())
    
    # Create SHA-256 hash
    hasher = hashlib.sha256()
    
    # Process each file
    for rel_path in files:
        # Get POSIX path as string and encode to UTF-8
        posix_path = rel_path.as_posix()
        path_bytes = posix_path.encode('utf-8')
        path_len = len(path_bytes)
        
        # Read file content
        full_path = path_obj / rel_path
        content_bytes = full_path.read_bytes()
        content_len = len(content_bytes)
        
        # Feed into hash: len:path len:content
        hasher.update(f"{path_len}:".encode('utf-8'))
        hasher.update(path_bytes)
        hasher.update(f"{content_len}:".encode('utf-8'))
        hasher.update(content_bytes)
    
    return hasher.hexdigest()
