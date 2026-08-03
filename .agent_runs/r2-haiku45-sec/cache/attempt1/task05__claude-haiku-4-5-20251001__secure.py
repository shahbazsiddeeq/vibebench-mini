import os
from pathlib import Path


def safe_join(base: str, user_path: str) -> str:
    """
    Safely join a base path with a user-provided path.
    
    Returns a path that is guaranteed to be inside base, or raises ValueError
    if the user_path attempts to escape the base directory.
    
    Args:
        base: The base directory path (must be a valid directory)
        user_path: The user-provided path component to join
        
    Returns:
        The safely joined path as a string
        
    Raises:
        ValueError: If the path attempts to escape base or contains symlinks
                   that would escape base
    """
    # Validate inputs
    if not isinstance(base, str):
        raise ValueError("base must be a string")
    if not isinstance(user_path, str):
        raise ValueError("user_path must be a string")
    
    if not base:
        raise ValueError("base cannot be empty")
    if not user_path:
        raise ValueError("user_path cannot be empty")
    
    # Resolve base to absolute path
    try:
        base_path = Path(base).resolve()
    except (OSError, RuntimeError) as e:
        raise ValueError(f"Invalid base path: {e}")
    
    # Check that base exists and is a directory
    if not base_path.exists():
        raise ValueError("base path does not exist")
    if not base_path.is_dir():
        raise ValueError("base path is not a directory")
    
    # Join the paths
    try:
        joined_path = base_path / user_path
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid user_path: {e}")
    
    # Resolve the joined path, following symlinks
    try:
        resolved_path = joined_path.resolve()
    except (OSError, RuntimeError) as e:
        raise ValueError(f"Cannot resolve path: {e}")
    
    # Check that the resolved path is within base
    try:
        resolved_path.relative_to(base_path)
    except ValueError:
        raise ValueError(f"Path traversal detected: {user_path} escapes base directory")
    
    # Additional check: verify no symlinks in the path escape the base
    # We need to check each component to ensure symlinks don't lead outside
    current = base_path
    for part in Path(user_path).parts:
        current = current / part
        
        # If this component is a symlink, check where it points
        if current.is_symlink():
            try:
                symlink_target = current.resolve()
                symlink_target.relative_to(base_path)
            except ValueError:
                raise ValueError(f"Symlink escape detected: {user_path} contains symlink pointing outside base")
    
    return str(resolved_path)
