import os


def find_by_ext(root, ext):
    if not ext.startswith("."):
        ext = "." + ext

    root_path = os.path.abspath(os.path.expanduser(root))
    matches = []

    for dirpath, _dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.endswith(ext):
                full_path = os.path.join(dirpath, filename)
                if os.path.isfile(full_path):
                    matches.append(os.path.realpath(full_path))

    return sorted(matches)
