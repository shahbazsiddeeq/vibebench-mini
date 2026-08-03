import hashlib


def sha256_file(path: str) -> str:
    """
    Returns the hex SHA-256 digest of a file's contents.
    
    Args:
        path: Path to the file
        
    Returns:
        Hex SHA-256 digest as a string
        
    Raises:
        FileNotFoundError: If the file does not exist
    """
    try:
        with open(path, 'rb') as f:
            sha256_hash = hashlib.sha256()
            # Read file in chunks to handle large files efficiently
            for chunk in iter(lambda: f.read(4096), b''):
                sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
