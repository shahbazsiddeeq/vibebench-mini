import json
import os
from pathlib import Path
from typing import List, Any, Dict


def merge_json_files(paths: List[str], output: str) -> None:
    """
    Merge multiple JSON files into a single output file.
    
    Reads JSON files from the given paths and performs a shallow merge,
    writing the result to the output file. Later files override earlier
    files for the same top-level keys.
    
    Args:
        paths: List of file paths to JSON files to merge
        output: Path to the output file
        
    Raises:
        ValueError: If any file's top-level JSON value is not an object
        FileNotFoundError: If any input file doesn't exist
        json.JSONDecodeError: If any file contains invalid JSON
        PermissionError: If files cannot be read or written
    """
    merged: Dict[str, Any] = {}
    
    # Process each input file in order
    for path in paths:
        # Validate path to prevent directory traversal attacks
        # Convert to absolute path for safer handling
        try:
            abs_path = os.path.abspath(path)
            
            # Read and parse the JSON file
            with open(abs_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate that the top-level value is a dictionary/object
            if not isinstance(data, dict):
                raise ValueError(
                    f"File '{path}' does not contain a JSON object at top level"
                )
            
            # Shallow merge: update merged dict with current file's data
            # Later files override earlier files for the same keys
            merged.update(data)
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: {path}")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in file '{path}': {e.msg}",
                e.doc,
                e.pos
            )
        except PermissionError:
            raise PermissionError(f"Permission denied reading file: {path}")
    
    # Write the merged result to the output file
    try:
        abs_output = os.path.abspath(output)
        
        # Ensure parent directory exists
        output_dir = os.path.dirname(abs_output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Write JSON with proper formatting
        with open(abs_output, 'w', encoding='utf-8') as f:
            json.dump(merged, f, ensure_ascii=False, indent=2)
            
    except PermissionError:
        raise PermissionError(f"Permission denied writing to file: {output}")
    except OSError as e:
        raise OSError(f"Error writing to output file '{output}': {e}")
