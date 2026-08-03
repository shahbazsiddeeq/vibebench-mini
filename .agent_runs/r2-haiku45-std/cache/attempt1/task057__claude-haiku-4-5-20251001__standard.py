import json


def merge_json_files(paths, output):
    """
    Merge a list of JSON files (each containing a JSON object) into a single file.
    
    The merge is SHALLOW: only top-level keys are combined. When the same top-level 
    key appears in more than one file, the value from the later file replaces the 
    earlier value entirely.
    
    Args:
        paths: List of file paths to JSON files (each must contain a JSON object)
        output: Output file path where the merged JSON will be written
        
    Raises:
        ValueError: If any file's top-level JSON value is not an object
    """
    merged = {}
    
    for path in paths:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Validate that the top-level value is an object (dict)
        if not isinstance(data, dict):
            raise ValueError(f"File {path} does not contain a JSON object at top level")
        
        # Shallow merge: update with new values from this file
        merged.update(data)
    
    # Write the merged result to output file
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(merged, f)
