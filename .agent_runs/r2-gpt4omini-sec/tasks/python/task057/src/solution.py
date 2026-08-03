import json
import os

def merge_json_files(paths, output):
    if not isinstance(paths, list):
        raise ValueError("paths must be a list")
    
    if not isinstance(output, str):
        raise ValueError("output must be a string representing a file path")
    
    merged_data = {}
    
    for path in paths:
        if not isinstance(path, str):
            raise ValueError("Each path must be a string")
        
        if not os.path.isfile(path):
            raise ValueError(f"File not found: {path}")
        
        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in file: {path}")
        
        if not isinstance(data, dict):
            raise ValueError(f"Top-level JSON value must be an object in file: {path}")
        
        merged_data.update(data)
    
    with open(output, 'w', encoding='utf-8') as outfile:
        json.dump(merged_data, outfile, ensure_ascii=False, indent=4)
