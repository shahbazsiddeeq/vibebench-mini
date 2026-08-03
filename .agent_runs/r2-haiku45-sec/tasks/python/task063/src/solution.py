import hashlib
from pathlib import Path


def sha256_file(path: str) -> str:
    """
    Compute the SHA-256 hash of a file's contents.
    
    Args:
        path: Path to the file to hash
        
    Returns:
        Hex digest of the file's SHA-256 hash
        
    Raises:
        FileNotFoundError: If the file does not exist
    """
    # Validate input is a string
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    
    # Convert to Path object for validation
    file_path = Path(path)
    
    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"No such file or directory: '{path}'")
    
    # Ensure it's a file, not a directory
    if not file_path.is_file():
        raise FileNotFoundError(f"Not a file: '{path}'")
    
    # Compute SHA-256 hash
    sha256_hash = hashlib.sha256()
    
    # Read file in chunks to handle large files efficiently
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            sha256_hash.update(chunk)
    
    return sha256_hash.hexdigest()
