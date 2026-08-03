class File:
    def __init__(self, name: str, size: int):
        self._validate_name(name)
        self._validate_size(size)
        self._name = name
        self._size = size

    @property
    def name(self) -> str:
        return self._name

    @property
    def size(self) -> int:
        return self._size

    def total_size(self) -> int:
        return self._size

    def _validate_name(self, name: str):
        if not isinstance(name, str) or not name:
            raise ValueError("Name must be a non-empty string.")
        if '/' in name:
            raise ValueError("Name cannot contain '/' character.")

    def _validate_size(self, size: int):
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            raise ValueError("Size must be a non-negative integer.")


class Directory:
    def __init__(self, name: str):
        self._validate_name(name)
        self._name = name
        self._children = {}

    @property
    def name(self) -> str:
        return self._name

    def add(self, child):
        if not isinstance(child, (File, Directory)):
            raise TypeError("Child must be an instance of File or Directory.")
        if child.name in self._children:
            raise ValueError(f"A child with the name '{child.name}' already exists in this directory.")
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
            elif isinstance(child, Directory):
                count += child.count_files()
        return count

    def list_paths(self) -> list[str]:
        paths = []
        for name, child in self._children.items():
            if isinstance(child, File):
                paths.append(name)
            elif isinstance(child, Directory):
                for sub_path in child.list_paths():
                    paths.append(f"{name}/{sub_path}")
        return sorted(paths)

    def _validate_name(self, name: str):
        if not isinstance(name, str) or not name:
            raise ValueError("Name must be a non-empty string.")
        if '/' in name:
            raise ValueError("Name cannot contain '/' character.")
