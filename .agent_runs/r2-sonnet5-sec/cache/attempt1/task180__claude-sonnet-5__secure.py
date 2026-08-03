"""Composite File System Tree.

A small, self-contained implementation of the Composite design pattern for a
simple in-memory file system model. Only standard library is used.
"""

from __future__ import annotations

from typing import Dict, List, Union


def _validate_name(name: str) -> str:
    """Validate a file/directory name.

    Rules:
      - must be a str
      - must be non-empty
      - must not contain the '/' character
    """
    if not isinstance(name, str):
        raise ValueError("name must be a string")
    if name == "":
        raise ValueError("name must be a non-empty string")
    if "/" in name:
        raise ValueError("name must not contain '/'")
    return name


def _validate_size(size: int) -> int:
    """Validate a file size.

    Rules:
      - must be an int (bool excluded, since bool is a subclass of int)
      - must be >= 0
    """
    if isinstance(size, bool) or not isinstance(size, int):
        raise ValueError("size must be an int")
    if size < 0:
        raise ValueError("size must be >= 0")
    return size


class File:
    """A leaf node representing a file."""

    __slots__ = ("name", "size")

    def __init__(self, name: str, size: int) -> None:
        self.name = _validate_name(name)
        self.size = _validate_size(size)

    def total_size(self) -> int:
        return self.size

    def __repr__(self) -> str:
        return f"File(name={self.name!r}, size={self.size!r})"


class Directory:
    """A composite node representing a directory containing files/directories."""

    __slots__ = ("name", "_children")

    def __init__(self, name: str) -> None:
        self.name = _validate_name(name)
        self._children: Dict[str, Union["File", "Directory"]] = {}

    def add(self, child: Union["File", "Directory"]) -> "Directory":
        if not isinstance(child, (File, Directory)):
            raise TypeError("child must be a File or Directory instance")
        if child.name in self._children:
            raise ValueError(
                f"a child with the name {child.name!r} already exists"
            )
        self._children[child.name] = child
        return self

    def total_size(self) -> int:
        total = 0
        for child in self._children.values():
            total += child.total_size()
        return total

    def count_files(self) -> int:
        count = 0
        for child in self._children.values():
            if isinstance(child, File):
                count += 1
            else:
                count += child.count_files()
        return count

    def list_paths(self) -> List[str]:
        paths: List[str] = []

        def _walk(node: "Directory", prefix: str) -> None:
            for name, child in node._children.items():
                path = f"{prefix}{name}" if prefix == "" else f"{prefix}/{name}"
                if isinstance(child, File):
                    paths.append(path)
                else:
                    _walk(child, path)

        _walk(self, "")
        return sorted(paths)

    def __repr__(self) -> str:
        return f"Directory(name={self.name!r}, children={list(self._children.keys())!r})"
