"""Utilities for splitting and joining binary files."""

from __future__ import annotations

import os
import secrets
from typing import BinaryIO

_COPY_BUFFER_SIZE = 1024 * 1024


def _validate_path(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if "\x00" in value:
        raise ValueError(f"{name} contains an invalid character")
    return value


def _write_all(destination: BinaryIO, data: bytes) -> None:
    view = memoryview(data)
    while view:
        written = destination.write(view)
        if written is None or written <= 0:
            raise OSError("failed to write file data")
        view = view[written:]


def split_file(path: str, chunk_size: int, dest_dir: str) -> list[str]:
    """Split a binary file into consecutively numbered chunk files."""
    path = _validate_path(path, "path")
    dest_dir = _validate_path(dest_dir, "dest_dir")

    if not isinstance(chunk_size, int):
        raise TypeError("chunk_size must be an integer")
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")

    created: list[str] = []
    basename = os.path.basename(path)

    # Opening first ensures a missing source raises before creating dest_dir.
    with open(path, "rb") as source:
        os.makedirs(dest_dir, exist_ok=True)

        index = 0
        while True:
            first = source.read(min(chunk_size, _COPY_BUFFER_SIZE))
            if not first:
                break

            part_path = os.path.join(
                dest_dir, f"{basename}.part{index:03d}"
            )
            remaining = chunk_size - len(first)
            reached_eof = False

            with open(part_path, "wb") as part:
                _write_all(part, first)

                while remaining:
                    block = source.read(min(remaining, _COPY_BUFFER_SIZE))
                    if not block:
                        reached_eof = True
                        break
                    _write_all(part, block)
                    remaining -= len(block)

            created.append(part_path)
            index += 1

            if reached_eof:
                break

    return created


def join_files(parts: list[str], dest: str) -> int:
    """Concatenate binary part files into dest and return bytes written."""
    if not isinstance(parts, list):
        raise TypeError("parts must be a list")

    validated_parts: list[str] = []
    for part in parts:
        validated = _validate_path(part, "part path")
        if not os.path.exists(validated):
            raise FileNotFoundError(validated)
        validated_parts.append(validated)

    dest = _validate_path(dest, "dest")
    parent = os.path.dirname(os.path.abspath(dest))
    temp_path: str | None = None

    try:
        for _ in range(100):
            candidate = os.path.join(
                parent, f".join-{secrets.token_hex(16)}.tmp"
            )
            try:
                output = open(candidate, "xb")
            except FileExistsError:
                continue
            temp_path = candidate
            break
        else:
            raise OSError("unable to create temporary destination file")

        total = 0
        with output:
            for part_path in validated_parts:
                with open(part_path, "rb") as part:
                    while True:
                        block = part.read(_COPY_BUFFER_SIZE)
                        if not block:
                            break
                        _write_all(output, block)
                        total += len(block)

        os.replace(temp_path, dest)
        temp_path = None
        return total
    finally:
        if temp_path is not None:
            try:
                os.remove(temp_path)
            except FileNotFoundError:
                pass
            except OSError:
                pass
