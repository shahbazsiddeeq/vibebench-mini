import os

def split_file(path: str, chunk_size: int, dest_dir: str) -> list[str]:
    """
    Reads the binary file at `path` and writes consecutive chunks of at most
    `chunk_size` bytes each into `dest_dir`.

    Args:
        path: The path to the input binary file.
        chunk_size: The maximum size of each chunk.
        dest_dir: The directory where the chunks will be written.

    Returns:
        A list of paths to the created part files, in order.

    Raises:
        ValueError: If chunk_size < 1.
        FileNotFoundError: If `path` does not exist.
    """
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")

    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file or directory: '{path}'")

    os.makedirs(dest_dir, exist_ok=True)

    part_paths = []
    basename = os.path.basename(path)
    part_index = 0

    with open(path, 'rb') as f_in:
        while True:
            chunk = f_in.read(chunk_size)
            if not chunk:
                break

            part_filename = f"{basename}.part{format(part_index, '03d')}"
            part_path = os.path.join(dest_dir, part_filename)
            part_paths.append(part_path)

            with open(part_path, 'wb') as f_out:
                f_out.write(chunk)

            part_index += 1

    return part_paths

def join_files(parts: list[str], dest: str) -> int:
    """
    Concatenates the raw bytes of each file in `parts`, in the given order,
    into a single new file at `dest`.

    Args:
        parts: A list of paths to the part files to be joined.
        dest: The path to the output file.

    Returns:
        The total number of bytes written.

    Raises:
        FileNotFoundError: If any part path does not exist.
    """
    total_bytes_written = 0

    # Check if all part files exist before starting to write
    for part_path in parts:
        if not os.path.exists(part_path):
            raise FileNotFoundError(f"No such file or directory: '{part_path}'")

    with open(dest, 'wb') as f_out:
        for part_path in parts:
            with open(part_path, 'rb') as f_in:
                while True:
                    chunk = f_in.read(4096)  # Read in 4KB chunks
                    if not chunk:
                        break
                    f_out.write(chunk)
                    total_bytes_written += len(chunk)

    return total_bytes_written
