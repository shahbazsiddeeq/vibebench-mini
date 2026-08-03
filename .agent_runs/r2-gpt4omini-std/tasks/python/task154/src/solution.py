import os

def split_file(path: str, chunk_size: int, dest_dir: str) -> list[str]:
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file {path} does not exist.")
    
    os.makedirs(dest_dir, exist_ok=True)
    
    parts = []
    basename = os.path.basename(path)
    
    with open(path, 'rb') as file:
        part_number = 0
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            
            part_filename = os.path.join(dest_dir, f"{basename}.part{part_number:03d}")
            with open(part_filename, 'wb') as part_file:
                part_file.write(chunk)
            
            parts.append(part_filename)
            part_number += 1
    
    return parts

def join_files(parts: list[str], dest: str) -> int:
    total_bytes_written = 0
    
    if not parts:
        open(dest, 'wb').close()  # Create an empty file
        return total_bytes_written
    
    for part in parts:
        if not os.path.exists(part):
            raise FileNotFoundError(f"The part file {part} does not exist.")
        
        with open(part, 'rb') as part_file:
            data = part_file.read()
            total_bytes_written += len(data)
            with open(dest, 'ab') as dest_file:
                dest_file.write(data)
    
    return total_bytes_written
