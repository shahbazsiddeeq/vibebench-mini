import hashlib
import os


def find_duplicates(root):
    hashes = {}
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if not os.path.isfile(filepath):
                continue
            h = hashlib.sha256()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    h.update(chunk)
            digest = h.hexdigest()
            hashes.setdefault(digest, []).append(filepath)
    return {k: v for k, v in hashes.items() if len(v) >= 2}
