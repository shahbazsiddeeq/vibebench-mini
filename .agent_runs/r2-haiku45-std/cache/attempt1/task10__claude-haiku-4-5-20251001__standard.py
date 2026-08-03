import json
import yaml
from datetime import date, datetime


def yaml_to_json(path: str) -> str:
    """
    Read a UTF-8 YAML file and return a canonical JSON string.
    
    - Uses yaml.safe_load to prevent unsafe tag execution
    - Returns JSON with sorted keys and compact separators
    - Non-ASCII characters are preserved (ensure_ascii=False)
    - Non-JSON-serializable values are converted to strings
    - Empty YAML files return "null"
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Convert non-JSON-serializable types to strings
    def convert_value(obj):
        if obj is None:
            return None
        elif isinstance(obj, bool):
            return obj
        elif isinstance(obj, (int, float)):
            return obj
        elif isinstance(obj, str):
            return obj
        elif isinstance(obj, (date, datetime)):
            return str(obj)
        elif isinstance(obj, dict):
            return {k: convert_value(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [convert_value(item) for item in obj]
        else:
            # For any other non-JSON-serializable type, convert to string
            return str(obj)
    
    converted_data = convert_value(data)
    
    return json.dumps(
        converted_data,
        sort_keys=True,
        separators=(',', ':'),
        ensure_ascii=False
    )
