from __future__ import annotations


def _check_name(name: object) -> str:
    if not isinstance(name, str) or not name or "/" in name:
        raise ValueError("name must be a non-empty str without '/'")
    return name


class File:
    """Leaf node in the composite tree."""

    def __init__(self, name: str, size: int) -> None:
        self.name = _check_name(name)
        if isinstance(size, bool) or not isinstance(size, int) or size < 0:
            raise ValueError("size must be an int >= 0")
        self.size = size

    def total_size(self) -> int:
        return self.size


class Directory:
    """Composite node holding File and Directory children."""

    def __init__(self, name: str) -> None:
        self.name = _check_name(name)
        self._children: list[File | Directory] = []

    def add(self, child: File | Directory) -> "Directory":
        if not isinstance(child, (File, Directory)):
            raise TypeError("child must be a File or Directory")
        if any(c.name == child.name for c in self._children):
            raise ValueError(f"duplicate name: {child.name!r}")
        self._children.append(child)
        return self

    def total_size(self) -> int:
        return sum(c.total_size() for c in self._children)

    def count_files(self) -> int:
        total = 0
        for c in self._children:
            if isinstance(c, File):
                total += 1
            else:
                total += c.count_files()
        return total

    def list_paths(self) -> list[str]:
        paths: list[str] = []
        for c in self._children:
            if isinstance(c, File):
                paths.append(c.name)
            else:
                paths.extend(f"{c.name}/{p}" for p in c.list_paths())
        return sorted(paths)
