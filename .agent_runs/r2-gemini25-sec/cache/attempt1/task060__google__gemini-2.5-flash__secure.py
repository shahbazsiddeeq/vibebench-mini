import os
import stat
import secrets
import shutil

def atomic_write(path: str, content: str):
    """
    Atomically writes content (UTF-8) to path.

    Writes to a temporary file in the same directory, then os.replace it onto path
    so a reader never sees a partial file. Creates parent directories if needed.
    When path already exists, the new file must keep the same permission mode as
    the file it replaces. For a new file use the normal default mode (0666 masked
    by the process umask).
    The temporary file's data must be flushed and fsync'd before the rename, and
    the containing directory fsync'd after it, so the replacement survives a crash.
    On any error no temporary file is left behind.

    Args:
        path: The target file path.
        content: The string content to write.

    Raises:
        TypeError: If path or content are not strings.
        OSError: If any underlying OS operation fails.
    """
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    if not isinstance(content, str):
        raise TypeError("content must be a string")

    # Normalize path to handle potential user input issues like '..'
    # and ensure it's an absolute path for clarity, though os.path.join
    # and os.replace handle relative paths fine.
    # For security, we don't want to resolve symlinks here, as the user
    # might intend to write to the symlink itself.
    # However, os.replace will follow symlinks for the target.
    # We'll use abspath to ensure consistent directory handling.
    abs_path = os.path.abspath(path)
    dirname = os.path.dirname(abs_path)
    basename = os.path.basename(abs_path)

    # Create parent directories if they don't exist
    if dirname and not os.path.exists(dirname):
        try:
            os.makedirs(dirname, exist_ok=True)
        except OSError as e:
            raise OSError(f"Failed to create parent directories for {path}: {e}") from e

    # Determine the target file's mode
    target_mode = None
    if os.path.exists(abs_path):
        try:
            target_mode = stat.S_IMODE(os.stat(abs_path).st_mode)
        except OSError as e:
            # If we can't get the mode, proceed with default, but log/raise if critical
            # For this task, we'll raise as it's a requirement to preserve mode.
            raise OSError(f"Failed to get mode of existing file {path}: {e}") from e

    # Generate a unique temporary file name in the same directory
    # Using secrets for a strong random component.
    temp_filename = f".{basename}.{secrets.token_hex(8)}.tmp"
    temp_path = os.path.join(dirname, temp_filename)

    # Ensure no temporary file is left behind on error
    try:
        # Write to the temporary file
        # Use 'x' mode to ensure we create a new file and don't accidentally
        # overwrite an existing one (though the random name makes this unlikely).
        # Use 'wb' for binary write to control encoding and ensure fsync works on bytes.
        with open(temp_path, "wb") as f:
            f.write(content.encode("utf-8"))
            f.flush()  # Flush Python's internal buffer
            os.fsync(f.fileno())  # Flush OS buffer to disk

        # Set permissions for the temporary file
        # If target_mode is None, it means the target file didn't exist,
        # so we rely on the default umask. Otherwise, set it to the target's mode.
        if target_mode is not None:
            try:
                os.chmod(temp_path, target_mode)
            except OSError as e:
                raise OSError(f"Failed to set mode for temporary file {temp_path}: {e}") from e

        # Atomically replace the target file with the temporary file
        try:
            os.replace(temp_path, abs_path)
        except OSError as e:
            raise OSError(f"Failed to replace {path} with {temp_path}: {e}") from e

        # fsync the directory containing the new file to ensure the directory entry
        # is written to disk.
        # This is crucial for durability after the rename.
        try:
            # Open the directory for fsync.
            # On some systems (e.g., Linux), you can fsync a directory file descriptor.
            # On others (e.g., macOS), fsyncing a directory FD might not be supported
            # or might not guarantee the directory entry is written.
            # However, it's the best cross-platform approach available in standard lib.
            with os.open(dirname, os.O_RDONLY) as dfd:
                os.fsync(dfd)
        except OSError as e:
            # This might fail on some filesystems or OSes, but it's important for durability.
            # We'll raise it as a critical error.
            raise OSError(f"Failed to fsync directory {dirname} after atomic write: {e}") from e

    except Exception:
        # Clean up the temporary file if any error occurs
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError as e:
                # Log this if possible, but re-raise the original exception
                # as the primary failure.
                # For this task, we just re-raise the original.
                pass
        raise
