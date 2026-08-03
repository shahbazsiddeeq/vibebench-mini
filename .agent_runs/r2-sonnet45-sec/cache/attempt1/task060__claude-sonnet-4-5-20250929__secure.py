import os
import tempfile
from pathlib import Path


def atomic_write(path: str, content: str) -> None:
    """
    Write content to path atomically using a temporary file and os.replace.
    
    - Writes to a temporary file in the same directory
    - Preserves existing file permissions if file exists
    - Creates parent directories if needed
    - Flushes and fsyncs data before rename
    - Fsyncs directory after rename for durability
    - Cleans up temp file on any error
    
    Args:
        path: Target file path
        content: UTF-8 content to write
    """
    # Validate inputs
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    
    path_obj = Path(path)
    parent_dir = path_obj.parent
    
    # Create parent directories if needed
    parent_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if target file exists and get its mode
    existing_mode = None
    try:
        stat_info = os.stat(path)
        existing_mode = stat_info.st_mode
    except FileNotFoundError:
        pass
    
    # Create temporary file in the same directory as target
    # This ensures atomic rename on the same filesystem
    temp_fd = None
    temp_path = None
    
    try:
        # Create temp file with restrictive permissions initially
        temp_fd = tempfile.mkstemp(
            dir=str(parent_dir),
            prefix='.tmp_',
            suffix='.tmp'
        )
        temp_path = temp_fd[1]
        fd = temp_fd[0]
        
        # Write content as UTF-8
        content_bytes = content.encode('utf-8')
        os.write(fd, content_bytes)
        
        # Flush and fsync the file data
        os.fsync(fd)
        
        # If replacing an existing file, preserve its permissions
        if existing_mode is not None:
            os.chmod(temp_path, existing_mode)
        else:
            # For new files, use default permissions (0666 & ~umask)
            # The temp file was created with restrictive permissions,
            # so we need to set it to the default
            # We'll let the umask handle the actual permissions
            os.chmod(temp_path, 0o666)
        
        # Close the file descriptor before rename
        os.close(fd)
        temp_fd = None
        
        # Atomically replace the target file
        os.replace(temp_path, path)
        
        # Fsync the directory to ensure the rename is durable
        try:
            dir_fd = os.open(str(parent_dir), os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
        except (OSError, AttributeError):
            # Some systems may not support directory fsync
            # Continue anyway as the file write itself was synced
            pass
        
        temp_path = None  # Successfully renamed, no cleanup needed
        
    except Exception:
        # Clean up temp file on any error
        if temp_fd is not None and temp_fd[0] >= 0:
            try:
                os.close(temp_fd[0])
            except OSError:
                pass
        
        if temp_path is not None:
            try:
                os.unlink(temp_path)
            except OSError:
                pass
        
        raise
