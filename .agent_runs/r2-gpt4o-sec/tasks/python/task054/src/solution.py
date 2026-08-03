import os
from typing import List

def find_by_ext(root: str, ext: str) -> List[str]:
    if not isinstance(root, str) or not isinstance(ext, str):
        raise ValueError("Both root and ext must be strings.")
    
    if not os.path.isdir(root):
        raise ValueError("The root must be a valid directory path.")
    
    # Normalize the extension to ensure it starts with a dot
    if not ext.startswith('.'):
        ext = '.' + ext
    
    matched_files = []
    
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(ext):
                full_path = os.path.abspath(os.path.join(dirpath, filename))
                matched_files.append(full_path)
    
    matched_files.sort()
    return matched_files
