import hashlib
import os
from collections import defaultdict


def find_duplicates(root):
    """
    Find duplicate files in a directory tree based on SHA-256 hash.
    
    Args:
        root: Root directory path to search
        
    Returns:
        Dict mapping SHA-256 hex hash to list of file paths with identical content.
        Only includes groups with 2 or more files.
    """
    hash_to_paths = defaultdict(list)
    
    # Walk through all files in the directory tree
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            
            # Skip if not a regular file (e.g., symlinks, special files)
            if not os.path.isfile(filepath):
                continue
                
            try:
                # Calculate SHA-256 hash of file content
                sha256_hash = hashlib.sha256()
                with open(filepath, 'rb') as f:
                    # Read in chunks to handle large files efficiently
                    while chunk := f.read(8192):
                        sha256_hash.update(chunk)
                
                file_hash = sha256_hash.hexdigest()
                hash_to_paths[file_hash].append(filepath)
            except (IOError, OSError):
                # Skip files that can't be read
                continue
    
    # Filter to only include groups with 2 or more files
    duplicates = {
        file_hash: paths 
        for file_hash, paths in hash_to_paths.items() 
        if len(paths) >= 2
    }
    
    return duplicates
