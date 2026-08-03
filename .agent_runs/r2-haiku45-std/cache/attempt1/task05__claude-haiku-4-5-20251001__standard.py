import os
from pathlib import Path


def safe_join(base, user_path):
    """
    Safely join a base path with a user-provided path.
    
    Returns a path that is guaranteed to be inside base.
    Rejects:
    - Absolute paths
    - Traversal attempts that escape base
    - Symlinks that point outside base
    
    Args:
        base: The base directory path (string)
        user_path: The user-provided path component (string)
    
    Returns:
        The safely joined path as a string
    
    Raises:
        ValueError: If the path attempts to escape base or contains unsafe symlinks
    """
    base_path = Path(base).resolve()
    
    # Join the paths
    joined = base_path / user_path
    
    # Resolve the joined path, following symlinks
    try:
        resolved = joined.resolve()
    except (OSError, RuntimeError):
        raise ValueError(f"Cannot resolve path: {user_path}")
    
    # Check if the resolved path is inside base
    try:
        resolved.relative_to(base_path)
    except ValueError:
        raise ValueError(f"Path traversal attempt detected: {user_path}")
    
    # Additional check: verify no symlinks in the path escape base
    # We need to check each component to catch symlink escapes
    current = base_path
    parts = Path(user_path).parts
    
    for part in parts:
        current = current / part
        
        # If this component is a symlink, check where it points
        if current.is_symlink():
            target = current.resolve()
            try:
                target.relative_to(base_path)
            except ValueError:
                raise ValueError(f"Symlink escape attempt detected: {user_path}")
    
    return str(resolved)
