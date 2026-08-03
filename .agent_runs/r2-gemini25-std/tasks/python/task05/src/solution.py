import os
from pathlib import Path

def safe_join(base: str, user_path: str) -> str:
    """
    Safely joins a base path with a user-provided path, preventing directory traversal.

    Args:
        base: The base directory path.
        user_path: The user-provided path to join.

    Returns:
        The securely joined path.

    Raises:
        ValueError: If the user_path attempts to traverse outside the base directory
                    or if a symlink within the user_path points outside the base.
    """
    base_path = Path(base).resolve()
    user_path_obj = Path(user_path)

    # Normalize the user_path to handle '..' and '.' components
    # but do not resolve it yet, as we need to check against the base.
    # We need to be careful with how we normalize to avoid resolving symlinks prematurely.
    # The goal is to get a path relative to base, then join and check.

    # First, ensure the user_path doesn't start with a root or '..'
    if user_path_obj.is_absolute() or user_path_obj.parts[0] == '..':
        raise ValueError("Absolute paths or paths starting with '..' are not allowed.")

    # Construct the full path by joining and then resolving
    # This resolution will follow symlinks and normalize '..' components
    full_path = (base_path / user_path_obj).resolve()

    # Check if the resolved full_path is still within the base_path
    try:
        full_path.relative_to(base_path)
    except ValueError:
        # This means full_path is not a subpath of base_path
        raise ValueError("Path attempts to traverse outside the base directory.")

    # Additional check for symlinks within the user_path that might point outside.
    # We need to iterate through the components of the user_path and check each one.
    current_check_path = base_path
    for part in user_path_obj.parts:
        if part == '.' or part == '':
            continue
        if part == '..':
            # This case is handled by the final relative_to check,
            # but we can also catch it here if it leads to an escape before resolution.
            # However, the resolve() and relative_to() check is more robust.
            pass
        else:
            potential_symlink_path = current_check_path / part
            if potential_symlink_path.is_symlink():
                resolved_symlink_target = potential_symlink_path.resolve()
                # If the symlink target is not within the base_path, it's an escape attempt
                try:
                    resolved_symlink_target.relative_to(base_path)
                except ValueError:
                    raise ValueError(f"Symlink '{part}' points outside the base directory.")
            current_check_path = current_check_path / part

    return str(full_path)
