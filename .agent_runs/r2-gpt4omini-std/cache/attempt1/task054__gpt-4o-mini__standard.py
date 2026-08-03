import os

def find_by_ext(root, ext):
    # Normalize the extension to ensure it starts with a dot
    if not ext.startswith('.'):
        ext = '.' + ext
    
    matched_files = []

    # Walk through the directory tree
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            # Check if the file ends with the specified extension
            if filename.endswith(ext):
                # Get the absolute path and add it to the list
                abs_path = os.path.abspath(os.path.join(dirpath, filename))
                matched_files.append(abs_path)

    # Return the sorted list of matched file paths
    return sorted(matched_files)
