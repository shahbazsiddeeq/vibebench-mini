import json
from typing import List

def merge_json_files(paths: List[str], output: str) -> None:
    merged = {}
    
    for path in paths:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if not isinstance(data, dict):
                raise ValueError(f"The top-level JSON value in {path} is not an object.")
            merged.update(data)
    
    with open(output, 'w', encoding='utf-8') as file:
        json.dump(merged, file)
