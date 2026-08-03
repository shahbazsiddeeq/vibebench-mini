import os
import tempfile
import shutil

def atomic_write(path, content):
    # Ensure the parent directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Determine the file mode if the file already exists
    if os.path.exists(path):
        existing_mode = os.stat(path).st_mode
    else:
        existing_mode = None

    # Create a temporary file in the same directory
    dir_name = os.path.dirname(path)
    fd, temp_path = tempfile.mkstemp(dir=dir_name)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as tmp_file:
            # Write content to the temporary file
            tmp_file.write(content)
            # Flush and fsync the file to ensure data is written to disk
            tmp_file.flush()
            os.fsync(tmp_file.fileno())

        # Replace the target file with the temporary file
        os.replace(temp_path, path)

        # If the file existed, restore its original permissions
        if existing_mode is not None:
            os.chmod(path, existing_mode)

        # Fsync the directory to ensure the rename is durable
        dir_fd = os.open(dir_name, os.O_DIRECTORY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)

    except Exception:
        # Ensure no temporary file is left behind on error
        try:
            os.remove(temp_path)
        except FileNotFoundError:
            pass
        raise
