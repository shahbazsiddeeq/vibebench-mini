import os
import hashlib

def dir_hash(path):
    if not os.path.isdir(path):
        raise ValueError("The provided path is not a directory.")
    
    # Create a SHA-256 hash object
    sha256 = hashlib.sha256()
    
    # Walk the directory tree
    for root, _, files in os.walk(path):
        for file in sorted(files):
            # Get the relative path
            rel_path = os.path.relpath(os.path.join(root, file), path)
            rel_path_bytes = rel_path.encode('utf-8')
            
            # Read the file content
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Update the hash with the formatted data
            sha256.update(f"{len(rel_path_bytes)}:".encode('utf-8'))
            sha256.update(rel_path_bytes)
            sha256.update(f"{len(content)}:".encode('utf-8'))
            sha256.update(content)
    
    # Return the hex digest of the hash
    return sha256.hexdigest()
