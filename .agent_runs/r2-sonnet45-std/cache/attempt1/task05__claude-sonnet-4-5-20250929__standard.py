import os
from pathlib import Path


def safe_join(base, user_path):
    """
    Safely join base and user_path, ensuring the result stays within base.
    
    Args:
        base: The base directory path
        user_path: The user-provided path to join
        
    Returns:
        The safely joined path as a string
        
    Raises:
        ValueError: If the resulting path would escape the base directory
    """
    # Convert to Path objects and resolve base to absolute path
    base_path = Path(base).resolve()
    
    # Join the paths
    joined_path = base_path / user_path
    
    # Resolve the joined path (follows symlinks and resolves ..)
    try:
        resolved_path = joined_path.resolve()
    except (OSError, RuntimeError):
        # Handle cases where resolution fails
        raise ValueError("Invalid path")
    
    # Check if the resolved path is within the base directory
    # We need to check if resolved_path is a subpath of base_path
    try:
        resolved_path.relative_to(base_path)
    except ValueError:
        # relative_to raises ValueError if resolved_path is not relative to base_path
        raise ValueError("Path traversal detected")
    
    return str(resolved_path)
