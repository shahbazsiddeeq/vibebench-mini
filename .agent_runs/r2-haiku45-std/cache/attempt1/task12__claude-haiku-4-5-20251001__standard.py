import hashlib
import os
from pathlib import Path


def dir_hash(path: str) -> str:
    """
    Returns a deterministic SHA-256 hex digest over the contents of a directory tree.
    
    Recursively collects every regular file under path, sorts by relative POSIX path,
    and feeds into a single SHA-256 hash:
    - byte length of UTF-8 relative path + colon + path bytes
    - byte length of file content + colon + content bytes
    
    Args:
        path: Path to a directory
        
    Returns:
        SHA-256 hex digest
        
    Raises:
        ValueError: if path is not a directory
    """
    path_obj = Path(path)
    
    if not path_obj.is_dir():
        raise ValueError(f"{path} is not a directory")
    
    # Collect all regular files with their relative paths
    files = []
    for root, dirs, filenames in os.walk(path_obj):
        for filename in filenames:
            file_path = Path(root) / filename
            if file_path.is_file():
                rel_path = file_path.relative_to(path_obj)
                # Convert to POSIX path (forward slashes)
                posix_path = rel_path.as_posix()
                files.append(posix_path)
    
    # Sort by relative POSIX path
    files.sort()
    
    # Create hash
    hasher = hashlib.sha256()
    
    for rel_path_str in files:
        # Encode path to UTF-8 bytes
        path_bytes = rel_path_str.encode('utf-8')
        
        # Add length-delimited path
        path_length = str(len(path_bytes)).encode('utf-8')
        hasher.update(path_length)
        hasher.update(b':')
        hasher.update(path_bytes)
        
        # Read file content
        file_full_path = path_obj / rel_path_str
        content = file_full_path.read_bytes()
        
        # Add length-delimited content
        content_length = str(len(content)).encode('utf-8')
        hasher.update(content_length)
        hasher.update(b':')
        hasher.update(content)
    
    return hasher.hexdigest()
