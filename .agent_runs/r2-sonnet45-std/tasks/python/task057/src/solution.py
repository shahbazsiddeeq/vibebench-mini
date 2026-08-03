import json


def merge_json_files(paths, output):
    """
    Merge JSON files with shallow merge strategy.
    
    Args:
        paths: List of file paths to JSON files (each must contain a JSON object)
        output: Output file path where merged JSON will be written
    
    Raises:
        ValueError: If any file's top-level JSON value is not an object
    """
    merged = {}
    
    for path in paths:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Validate that the top-level value is an object (dict in Python)
        if not isinstance(data, dict):
            raise ValueError(f"File {path} does not contain a JSON object at top level")
        
        # Shallow merge: update merged dict with data from current file
        # Later files override earlier ones
        merged.update(data)
    
    # Write the merged result to output file
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(merged, f)
