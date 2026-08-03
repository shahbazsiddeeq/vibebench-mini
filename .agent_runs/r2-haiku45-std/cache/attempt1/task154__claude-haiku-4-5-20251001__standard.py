import os


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
        ValueError: if chunk_size < 1
        FileNotFoundError: if path does not exist
    """
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    
    # Create destination directory if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)
    
    # Get the basename of the source file
    basename = os.path.basename(path)
    
    # Read the source file
    with open(path, 'rb') as f:
        file_data = f.read()
    
    # If file is empty, return empty list
    if len(file_data) == 0:
        return []
    
    # Split into chunks and write them
    parts = []
    part_index = 0
    
    for i in range(0, len(file_data), chunk_size):
        chunk = file_data[i:i + chunk_size]
        part_filename = f"{basename}.part{part_index:03d}"
        part_path = os.path.join(dest_dir, part_filename)
        
        with open(part_path, 'wb') as f:
            f.write(chunk)
        
        parts.append(part_path)
        part_index += 1
    
    return parts


def join_files(parts: list[str], dest: str) -> int:
    """
    Concatenate multiple files into a single output file.
    
    Args:
        parts: List of file paths to concatenate in order
        dest: Path to the output file
        
    Returns:
        Total number of bytes written
        
    Raises:
        FileNotFoundError: if any part file does not exist
    """
    # Check that all parts exist
    for part in parts:
        if not os.path.exists(part):
            raise FileNotFoundError(f"File not found: {part}")
    
    total_bytes = 0
    
    with open(dest, 'wb') as out_f:
        for part in parts:
            with open(part, 'rb') as in_f:
                data = in_f.read()
                out_f.write(data)
                total_bytes += len(data)
    
    return total_bytes
