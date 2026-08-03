import hashlib
import os


def sha256_file(path):
    """
    Returns the hex SHA-256 digest of a file's contents.
    
    Args:
        path: Path to the file to hash
        
    Returns:
        str: Hexadecimal SHA-256 digest of the file contents
        
    Raises:
        FileNotFoundError: If the file does not exist
    """
    # Validate input type
    if not isinstance(path, (str, bytes, os.PathLike)):
        raise TypeError("path must be a string, bytes, or PathLike object")
    
    # Convert to string for consistent handling
    path_str = os.fspath(path)
    
    # Check if file exists and raise FileNotFoundError if not
    if not os.path.exists(path_str):
        raise FileNotFoundError(f"No such file: '{path_str}'")
    
    # Check if path is a file (not a directory)
    if not os.path.isfile(path_str):
        raise IsADirectoryError(f"Path is not a file: '{path_str}'")
    
    # Create SHA-256 hash object
    sha256_hash = hashlib.sha256()
    
    # Read file in chunks to handle large files efficiently
    # and avoid loading entire file into memory
    chunk_size = 8192  # 8KB chunks
    
    try:
        with open(path_str, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                sha256_hash.update(chunk)
    except PermissionError as e:
        raise PermissionError(f"Permission denied: '{path_str}'") from e
    except OSError as e:
        raise OSError(f"Error reading file: '{path_str}'") from e
    
    # Return hexadecimal digest
    return sha256_hash.hexdigest()
