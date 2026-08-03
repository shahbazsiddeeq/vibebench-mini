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
    Durability: the temporary file's data must be flushed and fsync'd before the
    rename, and the containing directory fsync'd after it, so the replacement
    survives a crash. On any error no temporary file is left behind.

    Args:
        path: The target file path.
        content: The string content to write.

    Raises:
        ValueError: If path is not a string or is empty.
        OSError: If any underlying OS operation fails.
    """
    if not isinstance(path, str) or not path:
        raise ValueError("Path must be a non-empty string.")
    if not isinstance(content, str):
        raise ValueError("Content must be a string.")

    # Normalize path and get directory and filename
    path = os.path.abspath(path)
    dirname, filename = os.path.split(path)

    # Create parent directories if they don't exist
    if dirname and not os.path.exists(dirname):
        try:
            os.makedirs(dirname, exist_ok=True)
        except OSError as e:
            raise OSError(f"Failed to create parent directories for {path}: {e}") from e

    # Determine the mode for the new file
    original_mode = None
    if os.path.exists(path):
        try:
            original_mode = stat.S_IMODE(os.stat(path).st_mode)
        except OSError as e:
            raise OSError(f"Failed to get mode of existing file {path}: {e}") from e

    # Generate a unique temporary file name
    temp_filename = f".{filename}.{secrets.token_hex(8)}.tmp"
    temp_path = os.path.join(dirname, temp_filename)

    # Ensure no temporary file is left behind on error
    try:
        # Write to the temporary file
        # Use os.open with O_CREAT | O_EXCL for atomic creation and O_WRONLY
        # This also allows us to get a file descriptor for fsync.
        # Set mode to 0o600 for the temporary file to be private.
        fd = -1
        try:
            fd = os.open(temp_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, 'wb') as f:
                f.write(content.encode('utf-8'))
                f.flush()  # Ensure data is written to OS buffers
                os.fsync(f.fileno())  # Ensure data is written to disk
        except OSError as e:
            if fd != -1:
                os.close(fd) # Ensure fd is closed even if fdopen fails
            raise OSError(f"Failed to write to temporary file {temp_path}: {e}") from e

        # Set the correct permissions on the temporary file before replacing
        # This is important because os.replace might preserve permissions on some systems
        # or the target file might inherit permissions from the temp file.
        # We want the final file to have the correct permissions.
        if original_mode is not None:
            try:
                os.chmod(temp_path, original_mode)
            except OSError as e:
                raise OSError(f"Failed to set mode on temporary file {temp_path}: {e}") from e
        else:
            # If it's a new file, apply default umask
            # os.open already applied 0o600, so we need to adjust if umask allows more.
            # However, os.replace will typically inherit the mode of the temp file.
            # The most reliable way to ensure the final mode is correct for a new file
            # is to let os.open create it with 0o600, then chmod it to the desired
            # default (0o666 & ~umask) before the replace.
            # Python's default open() uses 0o666 & ~umask.
            # We can simulate this by getting the current umask.
            current_umask = os.umask(0)
            os.umask(current_umask) # Reset umask
            default_mode = 0o666 & ~current_umask
            try:
                os.chmod(temp_path, default_mode)
            except OSError as e:
                raise OSError(f"Failed to set default mode on temporary file {temp_path}: {e}") from e


        # Atomically replace the target file with the temporary file
        try:
            os.replace(temp_path, path)
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
            # The original code had `with os.open(dirname, os.O_RDONLY) as dfd:`,
            # which is correct for opening the directory. The TypeError indicates
            # that `dirname` was not a string, but an int. This implies `dirname`
            # was somehow overwritten or not correctly passed.
            # Re-checking the flow, `dirname` is derived from `path` and should be a string.
            # The error might have been from a test setup or a specific environment.
            # Let's ensure `dirname` is treated as a string for `os.open`.
            # The fix is to ensure `dirname` is indeed a string when passed to `os.open`.
            # The previous code was correct in its intent. The error suggests `dirname`
            # was not a string at that point.
            # Let's ensure `dirname` is a string.
            # The `os.open` function expects a path (string) as its first argument.
            # The error `TypeError: 'int' object does not support the context manager protocol`
            # implies that `os.open` itself returned an int (the file descriptor),
            # and then the `with` statement tried to use that int as a context manager.
            # This means `os.open` was called correctly, but the `with` statement
            # was incorrectly trying to use the *result* of `os.open` as the context manager,
            # instead of the `os.open` call itself.
            # The correct way to use `os.open` with a context manager is to wrap it
            # in a function that returns a context manager, or to use `os.fdopen`
            # after `os.open` if you need a file object.
            # However, for just `fsync`ing a directory, we just need the file descriptor.
            # So, we open it, fsync it, and close it.
            dir_fd = os.open(dirname, os.O_RDONLY)
            try:
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
        except OSError as e:
            # This is a durability concern, not a data integrity concern.
            # Log or raise, but the file content is already on disk.
            # For this task, we should raise.
            raise OSError(f"Failed to fsync directory {dirname} after atomic write: {e}") from e

    except Exception:
        # Clean up temporary file if any error occurred before successful replacement
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError as e:
                # Log this, but re-raise the original exception
                print(f"Warning: Failed to clean up temporary file {temp_path}: {e}")
        raise # Re-raise the original exception
