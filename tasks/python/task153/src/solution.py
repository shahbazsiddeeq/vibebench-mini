import hashlib
import os

_CHUNK = 65536


def checksum_manifest(root: str) -> dict[str, str]:
    """Return {relative_posix_path: sha256_hex} for every file under `root`."""
    if not os.path.exists(root):
        raise FileNotFoundError(root)
    if not os.path.isdir(root):
        raise NotADirectoryError(root)

    manifest: dict[str, str] = {}
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            manifest[rel] = _sha256_file(full)

    return {key: manifest[key] for key in sorted(manifest)}


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(_CHUNK)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()
