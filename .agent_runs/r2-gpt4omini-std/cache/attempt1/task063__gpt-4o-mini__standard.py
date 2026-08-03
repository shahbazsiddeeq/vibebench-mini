import hashlib
import os

def sha256_file(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"No such file: '{path}'")
    
    sha256_hash = hashlib.sha256()
    
    with open(path, "rb") as f:
        # Read the file in chunks to avoid using too much memory
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    
    return sha256_hash.hexdigest()
