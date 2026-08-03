import os
from pathlib import Path


def split_file(path: str, chunk_size: int, dest_dir: str) -> list[str]:
    """
    Split a binary file into chunks.
    
    Args:
        path: Path to the source file
        chunk_size: Maximum size of each chunk in bytes
        dest_dir: Destination directory for chunk files
        
    Returns:
        List of created part file paths in order
        
    Raises:
        ValueError: If chunk_size < 1
        FileNotFoundError: If path does not exist
    """
    # Validate chunk_size
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")
    
    # Validate that source file exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"Source file not found: {path}")
    
    # Create destination directory if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)
    
    # Get the basename of the source file
    basename = os.path.basename(path)
    
    # Read and split the file
    parts = []
    part_index = 0
    
    with open(path, 'rb') as src_file:
        while True:
            chunk = src_file.read(chunk_size)
            if not chunk:
                break
            
            # Create part filename with zero-padded index (at least 3 digits)
            part_filename = f"{basename}.part{format(part_index, '03d')}"
            part_path = os.path.join(dest_dir, part_filename)
            
            # Write chunk to part file
            with open(part_path, 'wb') as part_file:
                part_file.write(chunk)
            
            parts.append(part_path)
            part_index += 1
    
    return parts


def join_files(parts: list[str], dest: str) -> int:
    """
    Join multiple files into a single file.
    
    Args:
        parts: List of file paths to concatenate
        dest: Destination file path
        
    Returns:
        Total number of bytes written
        
    Raises:
        FileNotFoundError: If any part file does not exist
    """
    # Validate that all part files exist
    for part_path in parts:
        if not os.path.exists(part_path):
            raise FileNotFoundError(f"Part file not found: {part_path}")
    
    total_bytes = 0
    
    # Open destination file for writing
    with open(dest, 'wb') as dest_file:
        # Read each part file and write to destination
        for part_path in parts:
            with open(part_path, 'rb') as part_file:
                data = part_file.read()
                dest_file.write(data)
                total_bytes += len(data)
    
    return total_bytes
