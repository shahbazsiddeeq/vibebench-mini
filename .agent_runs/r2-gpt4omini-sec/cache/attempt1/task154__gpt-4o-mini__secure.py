# src/solution.py

import os
import secrets

def split_file(path: str, chunk_size: int, dest_dir: str) -> list[str]:
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")
    
    if not os.path.isfile(path):
        raise FileNotFoundError(f"The file {path} does not exist.")
    
    os.makedirs(dest_dir, exist_ok=True)
    
    parts = []
    basename = os.path.basename(path)
    
    with open(path, 'rb') as file:
        chunk_index = 0
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            
            part_filename = os.path.join(dest_dir, f"{basename}.part{chunk_index:03d}")
            with open(part_filename, 'wb') as part_file:
                part_file.write(chunk)
            
            parts.append(part_filename)
            chunk_index += 1
    
    return parts

def join_files(parts: list[str], dest: str) -> int:
    if not parts:
        with open(dest, 'wb') as dest_file:
            return 0
    
    total_bytes_written = 0
    
    for part in parts:
        if not os.path.isfile(part):
            raise FileNotFoundError(f"The part file {part} does not exist.")
        
        with open(part, 'rb') as part_file:
            data = part_file.read()
            total_bytes_written += len(data)
        
        with open(dest, 'ab') as dest_file:
            dest_file.write(data)
    
    return total_bytes_written
