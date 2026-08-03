import hashlib
import os
from pathlib import Path


def dir_hash(path: str) -> str:
    """
    Returns a deterministic SHA-256 hex digest over the contents of a directory tree.
    
    Recursively collects every regular file under path, ignores directories themselves,
    and sorts the files by their relative POSIX path (relative to path). For each file,
    feeds into a single SHA-256 hash, in order:
    - the byte length of the UTF-8 relative path followed by a colon
    - then the path bytes
    - then the byte length of the file content followed by a colon
    - then the content bytes
    
    Args:
        path: Path to the directory to hash
        
    Returns:
        SHA-256 hex digest string
        
    Raises:
        ValueError: if path is not a directory
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
    
    # Collect all regular files
    files = []
    
    try:
        for root, dirs, filenames in os.walk(path):
            root_path = Path(root)
            for filename in filenames:
                file_path = root_path / filename
                # Only include regular files
                if file_path.is_file():
                    # Calculate relative path
                    try:
                        rel_path = file_path.relative_to(path_obj)
                        # Convert to POSIX format for consistency
                        posix_path = rel_path.as_posix()
                        files.append((posix_path, file_path))
                    except ValueError:
                        # Skip files that can't be made relative
                        continue
    except (OSError, PermissionError) as e:
        raise ValueError(f"Error accessing directory: {e}")
    
    # Sort files by their relative POSIX path
    files.sort(key=lambda x: x[0])
    
    # Create hash
    hasher = hashlib.sha256()
    
    for posix_path, file_path in files:
        # Encode the relative path as UTF-8
        path_bytes = posix_path.encode('utf-8')
        path_length = len(path_bytes)
        
        # Read file content
        try:
            with open(file_path, 'rb') as f:
                content_bytes = f.read()
        except (OSError, PermissionError) as e:
            raise ValueError(f"Error reading file {posix_path}: {e}")
        
        content_length = len(content_bytes)
        
        # Feed into hash: length:path length:content
        hasher.update(f"{path_length}:".encode('utf-8'))
        hasher.update(path_bytes)
        hasher.update(f"{content_length}:".encode('utf-8'))
        hasher.update(content_bytes)
    
    return hasher.hexdigest()
