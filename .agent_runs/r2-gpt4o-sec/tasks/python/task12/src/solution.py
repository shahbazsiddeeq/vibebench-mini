import os
import hashlib

def dir_hash(path):
    if not os.path.isdir(path):
        raise ValueError("Provided path is not a directory")

    sha256 = hashlib.sha256()
    for root, _, files in os.walk(path):
        for file in sorted(files):
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, path).replace(os.sep, '/')
            rel_path_bytes = rel_path.encode('utf-8')
            file_content = open(file_path, 'rb').read()

            sha256.update(f"{len(rel_path_bytes)}:".encode('utf-8'))
            sha256.update(rel_path_bytes)
            sha256.update(f"{len(file_content)}:".encode('utf-8'))
            sha256.update(file_content)

    return sha256.hexdigest()
