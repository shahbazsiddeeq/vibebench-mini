import os


def split_file(path: str, chunk_size: int, dest_dir: str) -> list[str]:
    """Split a file into fixed-size byte chunks written into dest_dir."""
    if chunk_size < 1:
        raise ValueError("chunk_size must be >= 1")
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    os.makedirs(dest_dir, exist_ok=True)
    basename = os.path.basename(path)
    parts: list[str] = []

    with open(path, "rb") as src:
        index = 0
        while True:
            chunk = src.read(chunk_size)
            if not chunk:
                break
            part_path = os.path.join(dest_dir, f"{basename}.part{index:03d}")
            with open(part_path, "wb") as out:
                out.write(chunk)
            parts.append(part_path)
            index += 1

    return parts


def join_files(parts: list[str], dest: str) -> int:
    """Concatenate part files, in order, into dest. Return bytes written."""
    total = 0
    with open(dest, "wb") as out:
        for part in parts:
            with open(part, "rb") as src:
                while True:
                    chunk = src.read(65536)
                    if not chunk:
                        break
                    out.write(chunk)
                    total += len(chunk)
    return total
