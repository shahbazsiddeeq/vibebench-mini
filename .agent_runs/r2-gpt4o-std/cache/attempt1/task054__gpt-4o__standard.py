import os

def find_by_ext(root, ext):
    if not ext.startswith('.'):
        ext = '.' + ext

    matched_files = []

    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(ext):
                full_path = os.path.join(dirpath, filename)
                matched_files.append(os.path.abspath(full_path))

    return sorted(matched_files)
