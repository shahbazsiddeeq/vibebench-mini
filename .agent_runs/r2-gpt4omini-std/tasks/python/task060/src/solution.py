import os
import stat
import tempfile
import shutil

def atomic_write(path: str, content: str) -> None:
    # Get the directory and the filename
    dir_name = os.path.dirname(path)
    file_name = os.path.basename(path)

    # Create the directory if it doesn't exist
    os.makedirs(dir_name, exist_ok=True)

    # Determine the mode of the existing file if it exists
    if os.path.exists(path):
        existing_mode = stat.S_IMODE(os.stat(path).st_mode)
    else:
        existing_mode = None

    # Create a temporary file in the same directory
    with tempfile.NamedTemporaryFile('w', delete=False, dir=dir_name, encoding='utf-8') as temp_file:
        temp_file.write(content)
        temp_file.flush()
        os.fsync(temp_file.fileno())
        temp_file_path = temp_file.name

    # Replace the original file with the temporary file
    try:
        os.replace(temp_file_path, path)
    except Exception:
        os.remove(temp_file_path)
        raise

    # If the original file existed, restore its permissions
    if existing_mode is not None:
        os.chmod(path, existing_mode)

    # Fsync the directory to ensure durability
    dir_fd = os.open(dir_name, os.O_RDONLY)
    try:
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)
