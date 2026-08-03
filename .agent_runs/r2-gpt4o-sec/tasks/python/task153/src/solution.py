import os
import hashlib
from typing import Dict

def checksum_manifest(root: str) -> Dict[str, str]:
    if not os.path.exists(root):
        raise FileNotFoundError(f"The directory {root} does not exist.")
    if not os.path.isdir(root):
        raise NotADirectoryError(f"The path {root} is not a directory.")

    manifest = {}

    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(file_path, root).replace(os.sep, '/')
            sha256_hash = hashlib.sha256()

            try:
                with open(file_path, 'rb') as f:
                    for byte_block in iter(lambda: f.read(4096), b''):
                        sha256_hash.update(byte_block)
            except OSError:
                continue  # Skip files that can't be read

            manifest[relative_path] = sha256_hash.hexdigest()

    return dict(sorted(manifest.items()))
