import os
import stat
import tempfile


def atomic_write(path, content):
    path = os.fspath(path)
    directory = os.path.dirname(path)
    if directory == "":
        directory = "."
    os.makedirs(directory, exist_ok=True)

    existing_mode = None
    try:
        existing_mode = stat.S_IMODE(os.stat(path).st_mode)
    except OSError:
        existing_mode = None

    fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=".tmp-", suffix=".tmp")
    try:
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(content)
                f.flush()
                os.fsync(f.fileno())
        except BaseException:
            raise

        if existing_mode is not None:
            os.chmod(tmp_path, existing_mode)

        os.replace(tmp_path, path)

        dir_fd = os.open(directory, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    except BaseException:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
        raise
