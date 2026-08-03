"""Chunked File Splitter and Joiner."""

import os


def split_file(path: str, chunk_size: int, dest_dir: str) -> list:
    if chunk_size < 1:
        raise ValueError("chunk_size must be >= 1")
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file: {path}")

    os.makedirs(dest_dir, exist_ok=True)
    basename = os.path.basename(path)

    parts = []
    with open(path, "rb") as f:
        i = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            part_path = os.path.join(dest_dir, basename + ".part" + format(i, "03d"))
            with open(part_path, "wb") as pf:
                pf.write(chunk)
            parts.append(part_path)
            i += 1

    return parts


def join_files(parts: list, dest: str) -> int:
    for p in parts:
        if not os.path.exists(p):
            raise FileNotFoundError(f"No such file: {p}")

    total = 0
    with open(dest, "wb") as out:
        for p in parts:
            with open(p, "rb") as pf:
                data = pf.read()
                out.write(data)
                total += len(data)

    return total
