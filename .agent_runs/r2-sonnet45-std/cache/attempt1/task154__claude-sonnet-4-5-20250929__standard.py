import os


def split_file(path: str, chunk_size: int, dest_dir: str) -> list[str]:
    """
    Split a binary file into chunks.
    
    Args:
        path: Path to the source file
        chunk_size: Maximum size of each chunk in bytes
        dest_dir: Directory where chunks will be written
        
    Returns:
        List of paths to created chunk files
        
    Raises:
        ValueError: If chunk_size < 1
        FileNotFoundError: If path does not exist
    """
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    
    # Create destination directory if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)
    
    # Get the basename for naming parts
    basename = os.path.basename(path)
    
    parts = []
    part_index = 0
    
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            
            # Create part filename with at least 3-digit padding
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
    # Check that all parts exist before starting
    for part in parts:
        if not os.path.exists(part):
            raise FileNotFoundError(f"File not found: {part}")
    
    total_bytes = 0
    
    with open(dest, 'wb') as dest_file:
        for part in parts:
            with open(part, 'rb') as part_file:
                data = part_file.read()
                dest_file.write(data)
                total_bytes += len(data)
    
    return total_bytes
