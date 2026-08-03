import hashlib


def sha256_file(path):
    """
    Returns the hex SHA-256 digest of a file's contents.
    
    Args:
        path: Path to the file
        
    Returns:
        Hex string representation of the SHA-256 hash
        
    Raises:
        FileNotFoundError: If the file does not exist
    """
    sha256_hash = hashlib.sha256()
    
    with open(path, 'rb') as f:
        # Read the file in chunks to handle large files efficiently
        for chunk in iter(lambda: f.read(4096), b''):
            sha256_hash.update(chunk)
    
    return sha256_hash.hexdigest()
