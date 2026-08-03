def _validate_name(name: str) -> str:
    if not isinstance(name, str) or len(name) == 0 or '/' in name:
        raise ValueError("Invalid name: must be a non-empty string without '/'")
    return name


class File:
    def __init__(self, name: str, size: int):
        self.name = _validate_name(name)
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            raise ValueError("size must be a non-negative int")
        self.size = size

    def total_size(self) -> int:
        return self.size


class Directory:
    def __init__(self, name: str):
        self.name = _validate_name(name)
        self._children = {}

    def add(self, child):
        if not isinstance(child, (File, Directory)):
            raise TypeError("child must be a File or Directory")
        if child.name in self._children:
            raise ValueError(f"child with name '{child.name}' already exists")
        self._children[child.name] = child
        return self

    def total_size(self) -> int:
        return sum(child.total_size() for child in self._children.values())

    def count_files(self) -> int:
        count = 0
        for child in self._children.values():
            if isinstance(child, File):
                count += 1
            elif isinstance(child, Directory):
                count += child.count_files()
        return count

    def list_paths(self) -> list:
        paths = []
        for child in self._children.values():
            if isinstance(child, File):
                paths.append(child.name)
            elif isinstance(child, Directory):
                for p in child.list_paths():
                    paths.append(f"{child.name}/{p}")
        return sorted(paths)
