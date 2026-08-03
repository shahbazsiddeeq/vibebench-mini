import hashlib
import os

def sha256_file(path: str) -> str:
    # Validate the input path
    if not isinstance(path, str):
        raise ValueError("The path must be a string.")
    
    # Check if the file exists
    if not os.path.isfile(path):
        raise FileNotFoundError(f"The file '{path}' does not exist.")
    
    # Calculate the SHA-256 hash
    sha256_hash = hashlib.sha256()
    
    try:
        with open(path, "rb") as file:
            # Read the file in chunks to avoid memory issues with large files
            for byte_block in iter(lambda: file.read(4096), b""):
                sha256_hash.update(byte_block)
    except OSError as e:
        raise RuntimeError(f"An error occurred while reading the file: {e}")
    
    # Return the hex digest of the hash
    return sha256_hash.hexdigest()
