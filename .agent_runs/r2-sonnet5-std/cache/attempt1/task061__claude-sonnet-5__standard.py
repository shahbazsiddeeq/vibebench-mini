import os


def dir_size(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file or directory: '{path}'")
    if not os.path.isdir(path):
        raise NotADirectoryError(f"Not a directory: '{path}'")

    total = 0
    for root, dirs, files in os.walk(path):
        for name in files:
            full_path = os.path.join(root, name)
            if os.path.islink(full_path):
                continue
            if os.path.isfile(full_path):
                total += os.path.getsize(full_path)
    return total
