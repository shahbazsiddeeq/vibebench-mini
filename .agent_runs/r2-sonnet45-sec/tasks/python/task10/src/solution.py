import json
import yaml
from pathlib import Path
from datetime import date, datetime, time


def yaml_to_json(path):
    """
    Reads a UTF-8 YAML file and returns a canonical JSON string.
    
    Args:
        path: Path to the YAML file
        
    Returns:
        A JSON string with sorted keys, compact separators, and non-ASCII preserved
        
    Raises:
        yaml.YAMLError: If the YAML contains unsafe tags or is malformed
        FileNotFoundError: If the file doesn't exist
        PermissionError: If the file can't be read
    """
    # Validate input path
    if not isinstance(path, (str, Path)):
        raise TypeError("path must be a string or Path object")
    
    # Read the file with UTF-8 encoding
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        raise
    except PermissionError:
        raise
    except Exception as e:
        raise IOError(f"Failed to read file: {e}")
    
    # Parse YAML using safe_load to prevent code execution
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError:
        raise
    
    # Convert non-JSON-serializable types to strings
    data = _convert_to_json_serializable(data)
    
    # Convert to JSON with specified format
    json_str = json.dumps(
        data,
        sort_keys=True,
        separators=(',', ':'),
        ensure_ascii=False
    )
    
    return json_str


def _convert_to_json_serializable(obj):
    """
    Recursively convert objects to JSON-serializable types.
    Non-serializable types (like dates) are converted to strings.
    """
    if obj is None:
        return None
    elif isinstance(obj, bool):
        return obj
    elif isinstance(obj, (int, float, str)):
        return obj
    elif isinstance(obj, (date, datetime, time)):
        # Convert date/datetime/time objects to ISO format strings
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {
            _convert_to_json_serializable(k): _convert_to_json_serializable(v)
            for k, v in obj.items()
        }
    elif isinstance(obj, (list, tuple)):
        return [_convert_to_json_serializable(item) for item in obj]
    elif isinstance(obj, set):
        # Convert sets to sorted lists for deterministic output
        return sorted([_convert_to_json_serializable(item) for item in obj])
    else:
        # For any other type, convert to string
        return str(obj)
