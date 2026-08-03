import os
from pathlib import Path

def safe_join(base: str, user_path: str) -> str:
    """
    Safely joins a base path with a user-provided path, preventing directory
    traversal attacks.

    Args:
        base: The base directory path (e.g., a root for serving files).
        user_path: The user-provided path segment to append.

    Returns:
        The securely joined and normalized absolute path.

    Raises:
        ValueError: If the user_path attempts to traverse outside the base
                    directory, or if the resulting path is not within the
                    base directory after resolving symlinks.
        TypeError: If base or user_path are not strings.
    """
    if not isinstance(base, str):
        raise TypeError("base must be a string.")
    if not isinstance(user_path, str):
        raise TypeError("user_path must be a string.")

    # Normalize base path to an absolute path
    try:
        base_path = Path(base).resolve(strict=True)
    except FileNotFoundError:
        # If base path doesn't exist, we can't resolve it strictly.
        # We'll treat it as an absolute path for comparison, but the
        # subsequent checks will still ensure the joined path is within it.
        base_path = Path(base).resolve()
    except Exception as e:
        raise ValueError(f"Invalid base path '{base}': {e}") from e

    # Construct the full path by joining base and user_path
    # Use Path.joinpath for robust path segment joining
    full_path = base_path.joinpath(user_path)

    # Resolve the full path to handle '..' and symlinks
    # This is the critical step for security.
    # strict=True will raise FileNotFoundError if the path does not exist,
    # which is generally good for security as it prevents leaking information
    # about non-existent paths. However, the tests imply that we should
    # allow joining to non-existent files within the base.
    # So, we resolve without strict=True first, then check if it's still
    # within the base.
    try:
        resolved_full_path = full_path.resolve()
    except Exception as e:
        # If resolution fails for some reason (e.g., invalid characters,
        # but Path usually handles this), raise an error.
        raise ValueError(f"Could not resolve path '{full_path}': {e}") from e

    # Check if the resolved path is still a sub-path of the resolved base path.
    # This prevents directory traversal and symlink escape attacks.
    try:
        if not resolved_full_path.is_relative_to(base_path):
            raise ValueError(f"Attempted directory traversal: '{user_path}' resolves outside '{base}'")
    except AttributeError:
        # .is_relative_to() was added in Python 3.9.
        # For older versions, we can compare string representations.
        # This is less robust than is_relative_to but works for older Pythons.
        if not str(resolved_full_path).startswith(str(base_path) + os.sep) and \
           str(resolved_full_path) != str(base_path):
            raise ValueError(f"Attempted directory traversal: '{user_path}' resolves outside '{base}'")

    return str(resolved_full_path)
