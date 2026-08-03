import json
import os

def merge_json_files(paths, output):
    merged_data = {}

    for path in paths:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if not isinstance(data, dict):
                raise ValueError(f"The file {path} does not contain a JSON object.")
            merged_data.update(data)

    with open(output, 'w', encoding='utf-8') as file:
        json.dump(merged_data, file, ensure_ascii=False, indent=4)
