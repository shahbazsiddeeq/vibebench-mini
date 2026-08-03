import os
import secrets
import stat
from typing import Union

__all__ = ["atomic_write"]

PathType = Union[str, bytes, os.PathLike]


def atomic_write(path: PathType, content: str) -> None:
    """Atomically write UTF-8 text to a file."""
    target = os.fspath(path)
    data = content.encode("utf-8")

    directory = os.path.dirname(target)
    if not directory:
        directory = b"." if isinstance(target, bytes) else "."

    os.makedirs(directory, exist_ok=True)

    try:
        existing_mode = stat.S_IMODE(os.stat(target).st_mode)
    except FileNotFoundError:
        existing_mode = None

    basename = os.path.basename(target)
    temp_path = None
    fd = None

    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        flags |= getattr(os, "O_CLOEXEC", 0)
        flags |= getattr(os, "O_BINARY", 0)

        # Existing files begin private and receive their original mode after
        # writing. New files are created with the usual 0666 masked by umask.
        create_mode = 0o600 if existing_mode is not None else 0o666

        for _ in range(100):
            token = secrets.token_hex(12)
            if isinstance(target, bytes):
                temp_name = b"." + basename + b"." + token.encode("ascii") + b".tmp"
            else:
                temp_name = f".{basename}.{token}.tmp"
            candidate = os.path.join(directory, temp_name)

            try:
                fd = os.open(candidate, flags, create_mode)
            except FileExistsError:
                continue

            temp_path = candidate
            break
        else:
            raise FileExistsError("unable to create a unique temporary file")

        file_obj = os.fdopen(fd, "wb")
        fd = None
        with file_obj:
            file_obj.write(data)
            file_obj.flush()

            if existing_mode is not None:
                os.fchmod(file_obj.fileno(), existing_mode)

            os.fsync(file_obj.fileno())

        os.replace(temp_path, target)
        temp_path = None

        directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        directory_flags |= getattr(os, "O_CLOEXEC", 0)
        directory_fd = os.open(directory, directory_flags)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if fd is not None:
            try:
                os.close(fd)
            except OSError:
                pass

        if temp_path is not None:
            try:
                os.unlink(temp_path)
            except FileNotFoundError:
                pass
