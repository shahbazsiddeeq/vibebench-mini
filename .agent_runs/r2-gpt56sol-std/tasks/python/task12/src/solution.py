import hashlib
from pathlib import Path
from typing import Union


def dir_hash(path: Union[str, Path]) -> str:
    root = Path(path)
    if not root.is_dir():
        raise ValueError(f"Not a directory: {path}")

    files = sorted(
        (entry for entry in root.rglob("*") if entry.is_file()),
        key=lambda entry: entry.relative_to(root).as_posix(),
    )

    digest = hashlib.sha256()

    for file_path in files:
        relative_path = file_path.relative_to(root).as_posix().encode("utf-8")
        content = file_path.read_bytes()

        digest.update(str(len(relative_path)).encode("ascii"))
        digest.update(b":")
        digest.update(relative_path)
        digest.update(str(len(content)).encode("ascii"))
        digest.update(b":")
        digest.update(content)

    return digest.hexdigest()
