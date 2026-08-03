# src/solution.py

import os
from pathlib import Path

def safe_join(base: str, user_path: str) -> str:
    # Validate inputs
    if not isinstance(base, str) or not isinstance(user_path, str):
        raise ValueError("Both base and user_path must be strings.")
    
    # Normalize the base path
    base_path = Path(base).resolve()
    
    # Normalize the user path
    user_path_obj = (base_path / user_path).resolve()
    
    # Check if the resolved user path starts with the base path
    if not str(user_path_obj).startswith(str(base_path)):
        raise ValueError("Traversal attempt detected.")
    
    return str(user_path_obj)
