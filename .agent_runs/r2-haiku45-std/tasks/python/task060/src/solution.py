import os
import stat
import tempfile
from pathlib import Path


def atomic_write(path, content):
    """
    Atomically write content (UTF-8) to path.
    
    - Writes to a temporary file in the same directory, then replaces it onto path
    - Creates parent directories if needed
    - Preserves existing file permissions, or uses default for new files
    - Ensures durability with fsync on file and directory
    - Cleans up temp file on any error
    """
    path = str(path)
    parent_dir = os.path.dirname(path) or "."
    
    # Create parent directories if needed
    os.makedirs(parent_dir, exist_ok=True)
    
    # Check if target file exists and get its mode
    existing_mode = None
    if os.path.exists(path):
        existing_mode = stat.S_IMODE(os.stat(path).st_mode)
    
    # Create temporary file in the same directory as target
    temp_fd = None
    temp_path = None
    try:
        # Create temp file with restrictive permissions initially
        temp_fd, temp_path = tempfile.mkstemp(dir=parent_dir)
        
        # Write content to temp file
        with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
            f.write(content)
            # Flush and fsync to ensure durability
            f.flush()
            os.fsync(f.fileno())
        
        temp_fd = None  # fdopen closed it
        
        # If original file exists, preserve its mode
        if existing_mode is not None:
            os.chmod(temp_path, existing_mode)
        
        # Atomically replace the target file
        os.replace(temp_path, path)
        
        # Fsync the directory to ensure the rename is durable
        dir_fd = os.open(parent_dir, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
            
    except Exception:
        # Clean up temp file on any error
        if temp_fd is not None:
            try:
                os.close(temp_fd)
            except Exception:
                pass
        if temp_path is not None and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except Exception:
                pass
        raise
