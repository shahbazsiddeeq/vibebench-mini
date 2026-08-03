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
        Dictionary mapping SHA-256 hex hash to list of file paths.
        Only includes groups with 2 or more files.
    """
    hash_to_paths: Dict[str, List[str]] = {}
    
    # Walk through all files in the directory tree
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            
            # Calculate SHA-256 hash of the file
            try:
                file_hash = _sha256_file(filepath)
                
                # Add to dictionary
                if file_hash not in hash_to_paths:
                    hash_to_paths[file_hash] = []
                hash_to_paths[file_hash].append(filepath)
            except (OSError, IOError):
                # Skip files that can't be read
                continue
    
    # Filter to only include groups with 2+ files
    result = {
        file_hash: paths
        for file_hash, paths in hash_to_paths.items()
        if len(paths) >= 2
    }
    
    return result


def _sha256_file(filepath: str) -> str:
    """
    Calculate SHA-256 hash of a file.
    
    Args:
        filepath: Path to the file
        
    Returns:
        SHA-256 hex digest as a lowercase string
    """
    sha256_hash = hashlib.sha256()
    
    # Read file in chunks to handle large files efficiently
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256_hash.update(chunk)
    
    return sha256_hash.hexdigest()
