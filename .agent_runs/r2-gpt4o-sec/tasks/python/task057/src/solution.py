import json
import os

def merge_json_files(paths, output):
    if not isinstance(paths, list) or not all(isinstance(p, str) for p in paths):
        raise ValueError("Paths must be a list of strings.")
    if not isinstance(output, str):
        raise ValueError("Output must be a string.")

    merged_data = {}

    for path in paths:
        if not os.path.isfile(path):
            raise ValueError(f"File not found: {path}")
        
        with open(path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON in file: {path}")

            if not isinstance(data, dict):
                raise ValueError(f"Top-level JSON value must be an object in file: {path}")

            merged_data.update(data)

    with open(output, 'w', encoding='utf-8') as file:
        json.dump(merged_data, file, ensure_ascii=False, indent=4)
