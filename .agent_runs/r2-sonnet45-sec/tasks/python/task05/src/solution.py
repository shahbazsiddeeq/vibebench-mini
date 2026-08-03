import os
from pathlib import Path


def safe_join(base, user_path):
    """
    Safely join a base directory with a user-provided path.
    
    Returns an absolute path that is guaranteed to be inside the base directory.
    Raises ValueError if the resulting path would escape the base directory,
    including through symlinks.
    
    Args:
        base: The base directory path (string or Path-like)
        user_path: The user-provided path to join (string or Path-like)
    
    Returns:
        str: The absolute path inside base
        
    Raises:
        ValueError: If the path would escape base or if inputs are invalid
    """
    # Validate inputs
    if base is None or user_path is None:
        raise ValueError("base and user_path must not be None")
    
    # Convert to strings if needed
    try:
        base_str = str(base)
        user_path_str = str(user_path)
    except Exception:
        raise ValueError("base and user_path must be convertible to strings")
    
    # Check for empty strings
    if not base_str or not user_path_str:
        raise ValueError("base and user_path must not be empty")
    
    # Convert base to absolute path and resolve it
    try:
        base_path = Path(base_str).resolve()
    except Exception as e:
        raise ValueError(f"Invalid base path: {e}")
    
    # Join the paths
    try:
        # Use Path to handle the join operation
        joined_path = base_path / user_path_str
    except Exception as e:
        raise ValueError(f"Invalid user_path: {e}")
    
    # Resolve the joined path to handle . and .. components and symlinks
    try:
        resolved_path = joined_path.resolve()
    except Exception as e:
        raise ValueError(f"Cannot resolve path: {e}")
    
    # Check if the resolved path is inside the base directory
    # We need to ensure that resolved_path is a child of base_path
    try:
        # relative_to will raise ValueError if resolved_path is not relative to base_path
        resolved_path.relative_to(base_path)
    except ValueError:
        raise ValueError("Path traversal detected: resulting path is outside base directory")
    
    # Return as string
    return str(resolved_path)
