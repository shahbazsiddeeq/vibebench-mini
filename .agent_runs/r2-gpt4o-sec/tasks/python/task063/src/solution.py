import hashlib
import os

def sha256_file(path: str) -> str:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"The file at {path} does not exist.")
    
    sha256_hash = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
    except Exception as e:
        raise IOError("An error occurred while reading the file.") from e
    
    return sha256_hash.hexdigest()
