import os
import hashlib

def checksum_manifest(root: str) -> dict[str, str]:
    if not os.path.exists(root):
        raise FileNotFoundError(f"{root} does not exist")
    if not os.path.isdir(root):
        raise NotADirectoryError(f"{root} is not a directory")
    
    manifest = {}
    
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(file_path, root).replace(os.sep, '/')
            sha256 = hashlib.sha256()
            
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            
            manifest[relative_path] = sha256.hexdigest()
    
    return dict(sorted(manifest.items()))
