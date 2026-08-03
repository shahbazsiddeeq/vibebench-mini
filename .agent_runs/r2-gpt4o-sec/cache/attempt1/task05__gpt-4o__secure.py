import os
from pathlib import Path

def safe_join(base, user_path):
    # Resolve the base path to an absolute path
    base_path = Path(base).resolve(strict=True)
    
    # Join the base path with the user-provided path
    target_path = base_path.joinpath(user_path).resolve(strict=False)
    
    # Check if the resolved target path is within the base path
    if not target_path.is_relative_to(base_path):
        raise ValueError("Path traversal attempt detected")
    
    return str(target_path)
