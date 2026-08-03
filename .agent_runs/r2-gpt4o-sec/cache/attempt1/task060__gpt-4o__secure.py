import os
import tempfile
import shutil
import secrets

def atomic_write(path, content):
    # Ensure the parent directory exists
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    # Determine the file mode if the file already exists
    file_mode = None
    if os.path.exists(path):
        file_mode = os.stat(path).st_mode

    # Create a temporary file in the same directory
    temp_file = None
    try:
        temp_file = tempfile.NamedTemporaryFile(
            mode='w', 
            encoding='utf-8', 
            dir=dir_name, 
            delete=False
        )
        temp_file.write(content)
        temp_file.flush()
        os.fsync(temp_file.fileno())
        temp_file.close()

        # Set the file mode if the original file exists
        if file_mode is not None:
            os.chmod(temp_file.name, file_mode)

        # Atomically replace the target file with the temporary file
        os.replace(temp_file.name, path)

        # Ensure the directory entry is flushed
        dir_fd = os.open(dir_name, os.O_DIRECTORY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)

    except Exception as e:
        # Clean up the temporary file in case of any error
        if temp_file is not None:
            try:
                os.remove(temp_file.name)
            except OSError:
                pass
        raise e
