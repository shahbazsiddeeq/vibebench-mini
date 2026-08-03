import os


def split_file(path: str, chunk_size: int, dest_dir: str) -> list[str]:
    """Split a binary file into consecutively numbered chunk files."""
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")

    if not os.path.exists(path):
        raise FileNotFoundError(path)

    os.makedirs(dest_dir, exist_ok=True)

    basename = os.path.basename(path)
    parts: list[str] = []

    with open(path, "rb") as source:
        index = 0
        while True:
            chunk = source.read(chunk_size)
            if not chunk:
                break

            part_path = os.path.join(
                dest_dir, f"{basename}.part{index:03d}"
            )
            with open(part_path, "wb") as part_file:
                part_file.write(chunk)

            parts.append(part_path)
            index += 1

    return parts


def join_files(parts: list[str], dest: str) -> int:
    """Concatenate binary part files into dest and return bytes written."""
    for part_path in parts:
        if not os.path.exists(part_path):
            raise FileNotFoundError(part_path)

    total = 0
    buffer_size = 1024 * 1024

    with open(dest, "wb") as destination:
        for part_path in parts:
            with open(part_path, "rb") as part_file:
                while True:
                    chunk = part_file.read(buffer_size)
                    if not chunk:
                        break
                    destination.write(chunk)
                    total += len(chunk)

    return total
