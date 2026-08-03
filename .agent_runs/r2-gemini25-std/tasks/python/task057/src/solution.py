import json

def merge_json_files(paths, output):
    """
    Merges a list of UTF-8 JSON files into a single JSON file.

    The merge is SHALLOW: only top-level keys are combined. When the same top-level key appears
    in more than one file, the value from the later file in the list replaces the earlier value
    entirely, even if both values are themselves objects (no deep/recursive merge). Files are
    applied in list order, so the last file has highest precedence.

    Args:
        paths (list): A list of file paths to the JSON files to merge.
        output (str): The path to the output JSON file.

    Raises:
        ValueError: If any file's top-level JSON value is not an object.
    """
    merged_data = {}

    for path in paths:
        with open(path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"File '{path}' contains invalid JSON: {e}") from e

            if not isinstance(data, dict):
                raise ValueError(f"Top-level JSON value in file '{path}' is not an object.")
            
            merged_data.update(data)

    with open(output, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=None)
