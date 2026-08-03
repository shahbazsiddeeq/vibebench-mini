import os
import tempfile


def atomic_write(path, content):
    """
    Write content to path atomically.
    
    Args:
        path: Target file path
        content: UTF-8 string content to write
    """
    # Ensure parent directory exists
    parent_dir = os.path.dirname(path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)
    
    # Get the directory for the temp file (same as target)
    if parent_dir:
        temp_dir = parent_dir
    else:
        temp_dir = "."
    
    # Check if target exists and get its mode
    existing_mode = None
    if os.path.exists(path):
        existing_mode = os.stat(path).st_mode
    
    # Create temporary file in the same directory
    fd = None
    temp_path = None
    try:
        fd, temp_path = tempfile.mkstemp(dir=temp_dir, text=False)
        
        # Write content as UTF-8
        os.write(fd, content.encode('utf-8'))
        
        # Flush and fsync the file data
        os.fsync(fd)
        
        # If we're replacing an existing file, preserve its mode
        if existing_mode is not None:
            os.chmod(temp_path, existing_mode)
        
        # Close the file descriptor before rename
        os.close(fd)
        fd = None
        
        # Atomically replace the target file
        os.replace(temp_path, path)
        temp_path = None  # Successfully renamed, don't clean up
        
        # Fsync the directory to ensure the rename is durable
        dir_fd = os.open(temp_dir, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
            
    except:
        # Clean up on error
        if fd is not None:
            try:
                os.close(fd)
            except:
                pass
        if temp_path is not None and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except:
                pass
        raise
