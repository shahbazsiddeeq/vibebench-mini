import os
import stat
import tempfile
import shutil
import errno

def atomic_write(path: str, content: str) -> None:
    # Validate inputs
    if not isinstance(path, str) or not isinstance(content, str):
        raise ValueError("Both path and content must be strings.")
    
    # Ensure the content is UTF-8 encoded
    try:
        content_bytes = content.encode('utf-8')
    except UnicodeEncodeError:
        raise ValueError("Content must be UTF-8 encodable.")

    # Create the directory if it doesn't exist
    dir_name = os.path.dirname(path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # Create a temporary file in the same directory
    temp_fd, temp_path = tempfile.mkstemp(dir=dir_name, text=False)
    
    try:
        # Write content to the temporary file
        with os.fdopen(temp_fd, 'wb') as temp_file:
            temp_file.write(content_bytes)
            temp_file.flush()
            os.fsync(temp_file.fileno())  # Ensure data is flushed to disk

        # Get the existing file's mode if it exists
        existing_mode = None
        if os.path.exists(path):
            existing_mode = stat.S_IMODE(os.stat(path).st_mode)

        # Replace the original file with the temporary file
        os.replace(temp_path, path)

        # If there was an existing file, restore its permissions
        if existing_mode is not None:
            os.chmod(path, existing_mode)

        # Fsync the directory to ensure the change is durable
        dir_fd = os.open(dir_name, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)

    except Exception:
        # Clean up the temporary file if any error occurs
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise
