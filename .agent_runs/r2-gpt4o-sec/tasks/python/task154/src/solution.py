import os
from secrets import SystemRandom

def split_file(path: str, chunk_size: int, dest_dir: str) -> list[str]:
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file {path} does not exist")
    
    os.makedirs(dest_dir, exist_ok=True)
    basename = os.path.basename(path)
    part_paths = []
    
    with open(path, 'rb') as f:
        i = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            part_path = os.path.join(dest_dir, f"{basename}.part{format(i, '03d')}")
            with open(part_path, 'wb') as part_file:
                part_file.write(chunk)
            part_paths.append(part_path)
            i += 1
    
    return part_paths

def join_files(parts: list[str], dest: str) -> int:
    total_bytes_written = 0
    
    with open(dest, 'wb') as dest_file:
        for part in parts:
            if not os.path.exists(part):
                raise FileNotFoundError(f"The file {part} does not exist")
            
            with open(part, 'rb') as part_file:
                while True:
                    chunk = part_file.read(4096)
                    if not chunk:
                        break
                    dest_file.write(chunk)
                    total_bytes_written += len(chunk)
    
    return total_bytes_written
