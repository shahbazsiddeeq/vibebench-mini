import os
from pathlib import Path


def split_file(path: str, chunk_size: int, dest_dir: str) -> list[str]:
    """
    Split a binary file into chunks of at most chunk_size bytes each.
    
    Args:
        path: Path to the source file
        chunk_size: Maximum bytes per chunk (must be >= 1)
        dest_dir: Directory to write chunk files to
        
    Returns:
        List of created part file paths in order
        
    Raises:
        ValueError: If chunk_size < 1
        FileNotFoundError: If source file does not exist
    """
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    
    os.makedirs(dest_dir, exist_ok=True)
    
    basename = os.path.basename(path)
    parts = []
    
    with open(path, 'rb') as f:
        part_index = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            
            part_filename = f"{basename}.part{part_index:03d}"
            part_path = os.path.join(dest_dir, part_filename)
            
            with open(part_path, 'wb') as part_file:
                part_file.write(chunk)
            
            parts.append(part_path)
            part_index += 1
    
    return parts


def join_files(parts: list[str], dest: str) -> int:
    """
    Concatenate multiple files into a single output file.
    
    Args:
        parts: List of file paths to concatenate in order
        dest: Path to write the concatenated output
        
    Returns:
        Total number of bytes written
        
    Raises:
        FileNotFoundError: If any part file does not exist
    """
    total_bytes = 0
    
    with open(dest, 'wb') as out_file:
        for part_path in parts:
            if not os.path.exists(part_path):
                raise FileNotFoundError(f"Part file not found: {part_path}")
            
            with open(part_path, 'rb') as part_file:
                data = part_file.read()
                out_file.write(data)
                total_bytes += len(data)
    
    return total_bytes
