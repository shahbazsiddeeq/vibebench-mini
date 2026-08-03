"""Utilities for safely writing files atomically."""

import os
import secrets
import stat


_TEMP_ATTEMPTS = 100


def _create_temporary_file(directory):
    """Create a securely named temporary file in *directory*."""
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)

    for _ in range(_TEMP_ATTEMPTS):
        name = ".atomic-write-" + secrets.token_hex(16) + ".tmp"
        if isinstance(directory, bytes):
            name = name.encode("ascii")
        temporary_path = os.path.join(directory, name)

        try:
            fd = os.open(temporary_path, flags, 0o666)
        except FileExistsError:
            continue

        return fd, temporary_path

    raise FileExistsError("unable to create a unique temporary file")


def _fsync_directory(directory):
    """Synchronize directory metadata to durable storage."""
    flags = os.O_RDONLY
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_DIRECTORY", 0)

    directory_fd = os.open(directory, flags)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def atomic_write(path, content):
    """Atomically write UTF-8 text to a file.

    Parent directories are created as necessary. Existing file permissions are
    preserved, while new files receive the normal 0666 mode subject to umask.
    """
    try:
        file_path = os.fspath(path)
    except TypeError:
        raise TypeError("path must be a string or path-like object") from None

    if not isinstance(file_path, (str, bytes)):
        raise TypeError("path must resolve to a string or bytes")
    if not file_path:
        raise ValueError("path must not be empty")
    if (isinstance(file_path, str) and "\0" in file_path) or (
        isinstance(file_path, bytes) and b"\0" in file_path
    ):
        raise ValueError("path must not contain null bytes")
    if not isinstance(content, str):
        raise TypeError("content must be a string")

    encoded_content = content.encode("utf-8")

    directory = os.path.dirname(file_path)
    if not directory:
        directory = b"." if isinstance(file_path, bytes) else "."

    os.makedirs(directory, exist_ok=True)

    try:
        existing_mode = stat.S_IMODE(os.stat(file_path).st_mode)
    except FileNotFoundError:
        existing_mode = None

    fd = None
    temporary_path = None

    try:
        fd, temporary_path = _create_temporary_file(directory)

        stream = os.fdopen(fd, "wb")
        fd = None
        with stream:
            stream.write(encoded_content)
            stream.flush()

            if existing_mode is not None:
                os.fchmod(stream.fileno(), existing_mode)

            os.fsync(stream.fileno())

        os.replace(temporary_path, file_path)
        temporary_path = None

        _fsync_directory(directory)
    finally:
        if fd is not None:
            try:
                os.close(fd)
            except OSError:
                pass

        if temporary_path is not None:
            try:
                os.unlink(temporary_path)
            except FileNotFoundError:
                pass
            except OSError:
                pass
