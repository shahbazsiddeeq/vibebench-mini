# src/solution.py

import os
from pathlib import Path

def safe_join(base: str, user_path: str) -> str:
    # Resolve the base path to its absolute form
    base_path = Path(base).resolve()
    
    # Create a Path object for the user path
    user_path_obj = Path(user_path)
    
    # Resolve the user path to its absolute form
    resolved_user_path = (base_path / user_path_obj).resolve()
    
    # Check if the resolved user path starts with the base path
    if not str(resolved_user_path).startswith(str(base_path)):
        raise ValueError("Traversal attempt detected.")
    
    return str(resolved_user_path)
