import hashlib
import os
from typing import Union

PathLike = Union[str, bytes, os.PathLike]


def sha256_file(path: PathLike) -> str:
    """Return the lowercase hexadecimal SHA-256 digest of a file's contents."""
    digest = hashlib.sha256()
    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
