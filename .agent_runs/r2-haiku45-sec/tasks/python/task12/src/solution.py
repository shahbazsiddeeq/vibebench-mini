import hashlib
import os
from pathlib import Path


def dir_hash(path: str) -> str:
    """
    Returns a deterministic SHA-256 hex digest over the contents of a directory tree.
    
    Recursively collects every regular file under path, ignores directories themselves,
    and sorts files by their relative POSIX path. For each file, feeds into a single
    SHA-256 hash: the byte length of the UTF-8 relative path followed by a colon,
    then the path bytes, then the byte length of the file content followed by a colon,
    then the content bytes.
    
    Args:
        path: String path to a directory
        
    Returns:
        SHA-256 hex digest as a string
        
    Raises:
        ValueError: If path is not a directory
    """
    # Validate input
    if not isinstance(path, str):
        raise ValueError("path must be a string")
    
    path_obj = Path(path)
    
    # Check if path exists and is a directory
    if not path_obj.exists():
        raise ValueError(f"path does not exist: {path}")
    
    if not path_obj.is_dir():
        raise ValueError(f"path is not a directory: {path}")
    
    # Collect all regular files with their relative POSIX paths
    files = []
    try:
        for root, dirs, filenames in os.walk(path_obj):
            for filename in filenames:
                file_path = Path(root) / filename
                # Only process regular files
                if file_path.is_file():
                    # Get relative path and convert to POSIX format
                    rel_path = file_path.relative_to(path_obj)
                    posix_path = rel_path.as_posix()
                    files.append((posix_path, file_path))
    except (OSError, PermissionError) as e:
        raise ValueError(f"Error reading directory: {e}")
    
    # Sort files by their relative POSIX path
    files.sort(key=lambda x: x[0])
    
    # Create SHA-256 hash
    hasher = hashlib.sha256()
    
    # Process each file
    for posix_path, file_path in files:
        # Encode path to UTF-8
        path_bytes = posix_path.encode('utf-8')
        
        # Add path length and colon
        hasher.update(str(len(path_bytes)).encode('utf-8'))
        hasher.update(b':')
        
        # Add path bytes
        hasher.update(path_bytes)
        
        # Read file content
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
        except (OSError, PermissionError) as e:
            raise ValueError(f"Error reading file {file_path}: {e}")
        
        # Add content length and colon
        hasher.update(str(len(content)).encode('utf-8'))
        hasher.update(b':')
        
        # Add content bytes
        hasher.update(content)
    
    return hasher.hexdigest()
