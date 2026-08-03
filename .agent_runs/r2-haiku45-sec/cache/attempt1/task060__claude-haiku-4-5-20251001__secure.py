import os
import stat
import tempfile
from pathlib import Path


def atomic_write(path: str, content: str) -> None:
    """
    Atomically write content to a file.
    
    Writes content (UTF-8) to path atomically by writing to a temporary file
    in the same directory, then replacing the target path. Creates parent
    directories if needed. Preserves existing file permissions when overwriting.
    Ensures durability through fsync operations.
    
    Args:
        path: The target file path (string)
        content: The content to write (string, will be encoded as UTF-8)
    
    Raises:
        OSError: If file operations fail
        ValueError: If inputs are invalid
    """
    # Input validation
    if not isinstance(path, str):
        raise ValueError("path must be a string")
    if not isinstance(content, str):
        raise ValueError("content must be a string")
    
    if not path:
        raise ValueError("path cannot be empty")
    
    path = str(path)  # Ensure it's a string
    target_path = Path(path)
    parent_dir = target_path.parent
    
    # Create parent directories if needed
    parent_dir.mkdir(parents=True, exist_ok=True)
    
    # Get existing file mode if it exists
    existing_mode = None
    if target_path.exists():
        try:
            existing_mode = stat.S_IMODE(os.stat(path).st_mode)
        except OSError:
            # File might have been deleted between check and stat
            existing_mode = None
    
    # Create temporary file in the same directory as target
    temp_fd = None
    temp_path = None
    
    try:
        # Create temp file in same directory to ensure same filesystem
        temp_fd, temp_path = tempfile.mkstemp(
            dir=str(parent_dir),
            prefix='.tmp_',
            suffix=''
        )
        
        try:
            # Write content to temp file
            with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                f.write(content)
                # Flush to ensure data is written to OS buffer
                f.flush()
                # fsync to ensure data is written to disk
                os.fsync(f.fileno())
            
            temp_fd = None  # fdopen closed it
            
            # Set permissions on temp file if we're replacing an existing file
            if existing_mode is not None:
                os.chmod(temp_path, existing_mode)
            
            # Atomically replace target with temp file
            os.replace(temp_path, path)
            temp_path = None  # Successfully replaced, no cleanup needed
            
            # fsync the directory to ensure the rename is durable
            dir_fd = os.open(str(parent_dir), os.O_RDONLY)
            try:
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
                
        except Exception:
            # If fdopen hasn't been called yet, close the fd
            if temp_fd is not None:
                os.close(temp_fd)
            raise
            
    except Exception:
        # Clean up temp file if it still exists
        if temp_path is not None:
            try:
                os.unlink(temp_path)
            except OSError:
                pass
        raise
