import hashlib

def sha256_file(path):
    try:
        with open(path, 'rb') as f:
            file_content = f.read()
            sha256_hash = hashlib.sha256(file_content).hexdigest()
            return sha256_hash
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at path {path} was not found.")
