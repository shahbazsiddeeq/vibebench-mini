import json
import yaml
from datetime import date, datetime
from pathlib import Path


def yaml_to_json(path: str) -> str:
    """
    Read a UTF-8 YAML file and return a canonical JSON string.
    
    - Uses yaml.safe_load to prevent unsafe deserialization
    - Returns JSON with sorted keys and compact separators
    - Non-ASCII characters are preserved (ensure_ascii=False)
    - Non-JSON-serializable values are converted to strings
    - Empty YAML files (None) produce "null"
    
    Args:
        path: Path to the YAML file
        
    Returns:
        A JSON string representation of the YAML content
        
    Raises:
        yaml.YAMLError: If the YAML contains unsafe tags
        Various exceptions: If file cannot be read or parsed
    """
    # Validate input
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    
    # Read the YAML file
    path_obj = Path(path)
    with open(path_obj, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse YAML with safe loader (rejects unsafe tags)
    data = yaml.safe_load(content)
    
    # Convert to JSON with custom encoder for non-serializable types
    json_str = json.dumps(
        data,
        default=_json_serializer,
        sort_keys=True,
        separators=(',', ':'),
        ensure_ascii=False
    )
    
    return json_str


def _json_serializer(obj):
    """
    Custom JSON serializer for objects not serializable by default json code.
    Converts date/datetime and other non-JSON types to their string representation.
    
    Args:
        obj: Object to serialize
        
    Returns:
        String representation of the object
        
    Raises:
        TypeError: If object cannot be serialized
    """
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    
    # For other non-serializable types, convert to string
    return str(obj)
