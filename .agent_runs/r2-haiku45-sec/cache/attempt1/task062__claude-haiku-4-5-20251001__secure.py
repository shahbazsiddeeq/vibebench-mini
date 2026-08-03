import hashlib
import os
from pathlib import Path
from typing import Dict, List


def find_duplicates(root: str) -> Dict[str, List[str]]:
    """
    Find duplicate files in a directory tree based on SHA-256 content hash.
    
    Args:
        root: Root directory path to search for duplicates
        
    Returns:
        Dictionary mapping SHA-256 hex hash to list of file paths.
        Only includes groups with 2 or more files.
    """
    # Validate input
    if not isinstance(root, str):
        raise TypeError("root must be a string")
    
    root_path = Path(root)
    
    # Validate that root exists and is a directory
    if not root_path.exists():
        raise ValueError(f"Path does not exist: {root}")
    if not root_path.is_dir():
        raise ValueError(f"Path is not a directory: {root}")
    
    # Dictionary to store hash -> list of file paths
    hash_to_files: Dict[str, List[str]] = {}
    
    # Walk through all files in the directory tree
    try:
        for dirpath, dirnames, filenames in os.walk(root_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                
                # Skip if not a regular file (e.g., symlinks, directories)
                if not os.path.isfile(filepath):
                    continue
                
                try:
                    # Compute SHA-256 hash of file content
                    file_hash = _compute_sha256(filepath)
                    
                    # Add to dictionary
                    if file_hash not in hash_to_files:
                        hash_to_files[file_hash] = []
                    hash_to_files[file_hash].append(filepath)
                    
                except (OSError, IOError):
                    # Skip files that cannot be read
                    continue
    except (OSError, ValueError):
        # Handle permission errors or other OS errors gracefully
        pass
    
    # Filter to only include groups with 2 or more files
    result = {
        file_hash: paths
        for file_hash, paths in hash_to_files.items()
        if len(paths) >= 2
    }
    
    return result


def _compute_sha256(filepath: str) -> str:
    """
    Compute SHA-256 hash of a file's content.
    
    Args:
        filepath: Path to the file
        
    Returns:
        SHA-256 hex digest (64 lowercase hex characters)
    """
    sha256_hash = hashlib.sha256()
    
    # Read file in chunks to handle large files efficiently
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            sha256_hash.update(chunk)
    
    return sha256_hash.hexdigest()
