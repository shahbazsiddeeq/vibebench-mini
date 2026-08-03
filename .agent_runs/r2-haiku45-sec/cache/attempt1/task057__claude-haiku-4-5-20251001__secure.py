import json
from pathlib import Path


def merge_json_files(paths, output):
    """
    Merge multiple JSON files into a single output file.
    
    Reads UTF-8 JSON files from the given paths (each must contain a JSON object)
    and writes their shallow merge to the output file.
    
    The merge is SHALLOW: only top-level keys are combined. When the same top-level
    key appears in more than one file, the value from the later file replaces the
    earlier value entirely.
    
    Args:
        paths: List of file paths to JSON files to merge
        output: Path to write the merged JSON output
        
    Raises:
        ValueError: If any file's top-level JSON value is not an object (dict)
        FileNotFoundError: If any input file does not exist
        json.JSONDecodeError: If any file contains invalid JSON
    """
    merged = {}
    
    # Process each file in order
    for path in paths:
        try:
            # Read and parse the JSON file
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {path}") from e
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in file {path}: {e}") from e
        except Exception as e:
            raise ValueError(f"Error reading file {path}: {e}") from e
        
        # Validate that the top-level value is an object (dict)
        if not isinstance(data, dict):
            raise ValueError(
                f"File {path} does not contain a JSON object at top level"
            )
        
        # Shallow merge: update with all keys from this file
        # Later files override earlier ones
        merged.update(data)
    
    # Write the merged result to output file
    try:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(merged, f)
    except Exception as e:
        raise ValueError(f"Error writing to output file {output}: {e}") from e
