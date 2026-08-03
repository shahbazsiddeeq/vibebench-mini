import hashlib
import os


def checksum_manifest(root: str) -> dict:
    if not os.path.exists(root):
        raise FileNotFoundError(f"No such file or directory: {root!r}")
    if not os.path.isdir(root):
        raise NotADirectoryError(f"Not a directory: {root!r}")

    manifest = {}

    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            if os.path.islink(full_path):
                continue
            rel_path = os.path.relpath(full_path, root)
            key = rel_path.replace(os.sep, "/")

            hasher = hashlib.sha256()
            with open(full_path, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    hasher.update(chunk)
            manifest[key] = hasher.hexdigest()

    return dict(sorted(manifest.items()))
