from __future__ import annotations


def _validate_name(name: str) -> None:
    if not isinstance(name, str) or not name or "/" in name:
        raise ValueError("name must be a non-empty string without '/' characters")


class File:
    def __init__(self, name: str, size: int) -> None:
        _validate_name(name)
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            raise ValueError("size must be a non-negative integer")
        self.name = name
        self.size = size

    def total_size(self) -> int:
        return self.size


class Directory:
    def __init__(self, name: str) -> None:
        _validate_name(name)
        self.name = name
        self._children: dict[str, File | Directory] = {}

    def add(self, child: File | Directory) -> Directory:
        if not isinstance(child, (File, Directory)):
            raise TypeError("child must be a File or Directory")
        if child.name in self._children:
            raise ValueError(f"a child named {child.name!r} already exists")
        self._children[child.name] = child
        return self

    def total_size(self) -> int:
        return sum(child.total_size() for child in self._children.values())

    def count_files(self) -> int:
        return sum(
            1 if isinstance(child, File) else child.count_files()
            for child in self._children.values()
        )

    def list_paths(self) -> list[str]:
        paths: list[str] = []

        for child in self._children.values():
            if isinstance(child, File):
                paths.append(child.name)
            else:
                paths.extend(
                    f"{child.name}/{relative_path}"
                    for relative_path in child.list_paths()
                )

        return sorted(paths)
