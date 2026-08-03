import hashlib
import os
from pathlib import Path
from typing import Dict, List


def find_duplicates(root: str) -> Dict[str, List[str]]:
    """
    Find duplicate files in a directory tree based on SHA-256 hash.
    
    Args:
        root: Root directory path to search for duplicates
        
    Returns:
        Dictionary mapping SHA-256 hex hash to list of file paths with identical content.
        Only includes groups with 2 or more files.
    """
    # Validate input
    if not isinstance(root, str):
        raise TypeError("root must be a string")
    
    # Convert to Path object for safer path handling
    try:
        root_path = Path(root).resolve()
    except (ValueError, OSError) as e:
        raise ValueError(f"Invalid root path: {e}")
    
    # Check if path exists and is a directory
    if not root_path.exists():
        raise ValueError(f"Path does not exist: {root}")
    
    if not root_path.is_dir():
        raise ValueError(f"Path is not a directory: {root}")
    
    # Dictionary to store hash -> list of file paths
    hash_to_paths: Dict[str, List[str]] = {}
    
    # Walk through directory tree
    try:
        for dirpath, dirnames, filenames in os.walk(root_path):
            dirpath_obj = Path(dirpath)
            
            for filename in filenames:
                filepath = dirpath_obj / filename
                
                # Skip if not a regular file (e.g., symlinks, special files)
                try:
                    if not filepath.is_file():
                        continue
                    
                    # Calculate SHA-256 hash
                    file_hash = _calculate_sha256(filepath)
                    
                    # Store the path (as string)
                    if file_hash not in hash_to_paths:
                        hash_to_paths[file_hash] = []
                    hash_to_paths[file_hash].append(str(filepath))
                    
                except (OSError, PermissionError):
                    # Skip files we can't read
                    continue
    except (OSError, PermissionError):
        # If we can't walk the directory, return what we have so far
        pass
    
    # Filter to only include groups with 2+ files
    duplicates = {
        file_hash: paths 
        for file_hash, paths in hash_to_paths.items() 
        if len(paths) >= 2
    }
    
    return duplicates


def _calculate_sha256(filepath: Path) -> str:
    """
    Calculate SHA-256 hash of a file.
    
    Args:
        filepath: Path object pointing to the file
        
    Returns:
        Lowercase hexadecimal SHA-256 digest string
    """
    sha256_hash = hashlib.sha256()
    
    # Read file in chunks to handle large files efficiently
    chunk_size = 65536  # 64KB chunks
    
    try:
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                sha256_hash.update(chunk)
    except (OSError, PermissionError) as e:
        # Re-raise to be caught by caller
        raise
    
    return sha256_hash.hexdigest()
