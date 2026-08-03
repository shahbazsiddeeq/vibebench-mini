import os
from typing import List


def split_file(path: str, chunk_size: int, dest_dir: str) -> List[str]:
    """
    Reads the binary file at `path` and writes consecutive chunks of at most
    `chunk_size` bytes each into `dest_dir`.

    Part i (starting at 0) is written to os.path.join(dest_dir, basename + '.part' + format(i, '03d'))
    where basename is os.path.basename(path); indices pad to at least 3 digits (part000, part001, ...).
    It returns the list of created part paths in order.
    An empty input file produces zero parts and returns [].

    Raises ValueError if chunk_size < 1.
    Raises FileNotFoundError if `path` does not exist.
    """
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    if not isinstance(chunk_size, int):
        raise TypeError("chunk_size must be an integer")
    if not isinstance(dest_dir, str):
        raise TypeError("dest_dir must be a string")

    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Source file not found: {path}")
    if not os.path.isfile(path):
        raise ValueError(f"Path is not a file: {path}")

    os.makedirs(dest_dir, exist_ok=True)

    basename = os.path.basename(path)
    part_paths: List[str] = []
    part_index = 0

    try:
        with open(path, 'rb') as f_read:
            while True:
                chunk = f_read.read(chunk_size)
                if not chunk:
                    break

                part_filename = f"{basename}.part{format(part_index, '03d')}"
                part_path = os.path.join(dest_dir, part_filename)
                
                # Ensure part_path is within dest_dir to prevent path traversal
                if not os.path.commonprefix([os.path.realpath(part_path), os.path.realpath(dest_dir)]) == os.path.realpath(dest_dir):
                    raise ValueError(f"Generated part path '{part_path}' is outside of destination directory '{dest_dir}'")

                with open(part_path, 'wb') as f_write:
                    f_write.write(chunk)
                part_paths.append(part_path)
                part_index += 1
    except OSError as e:
        # Catch OS-related errors during file operations
        raise IOError(f"Error during file splitting: {e}") from e

    return part_paths


def join_files(parts: List[str], dest: str) -> int:
    """
    Concatenates the raw bytes of each file in `parts`, in the given order,
    into a single new file at `dest`, and returns the total number of bytes written.

    An empty `parts` list writes an empty file and returns 0.
    Raises FileNotFoundError if any part path does not exist.
    """
    if not isinstance(parts, list):
        raise TypeError("parts must be a list of strings")
    if not all(isinstance(p, str) for p in parts):
        raise TypeError("All elements in parts must be strings")
    if not isinstance(dest, str):
        raise TypeError("dest must be a string")

    total_bytes_written = 0

    # Validate all part paths exist before starting to write to dest
    for part_path in parts:
        if not os.path.exists(part_path):
            raise FileNotFoundError(f"Part file not found: {part_path}")
        if not os.path.isfile(part_path):
            raise ValueError(f"Part path is not a file: {part_path}")

    try:
        with open(dest, 'wb') as f_dest:
            for part_path in parts:
                try:
                    with open(part_path, 'rb') as f_part:
                        while True:
                            chunk = f_part.read(4096)  # Read in reasonable chunks
                            if not chunk:
                                break
                            f_dest.write(chunk)
                            total_bytes_written += len(chunk)
                except OSError as e:
                    # Catch OS-related errors during reading part files
                    raise IOError(f"Error reading part file '{part_path}': {e}") from e
    except OSError as e:
        # Catch OS-related errors during writing to destination file
        raise IOError(f"Error writing to destination file '{dest}': {e}") from e

    return total_bytes_written
