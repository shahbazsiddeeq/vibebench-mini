from pathlib import Path


def find_by_ext(root, ext):
    """Return sorted absolute paths of regular files with the given final suffix."""
    suffix = str(ext)
    if not suffix.startswith("."):
        suffix = "." + suffix

    root_path = Path(root).resolve()
    if not root_path.is_dir():
        return []

    matches = [
        str(path.resolve())
        for path in root_path.rglob("*")
        if path.is_file() and path.suffix == suffix
    ]
    return sorted(matches)
