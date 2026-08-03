import yaml
import json
from datetime import date, datetime, time


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder that converts dates/times to ISO format strings."""
    
    def default(self, obj):
        if isinstance(obj, (date, datetime, time)):
            return obj.isoformat()
        return super().default(obj)


def yaml_to_json(path):
    """
    Read a YAML file and convert it to canonical JSON string.
    
    Args:
        path: Path to the UTF-8 YAML file
        
    Returns:
        JSON string with sorted keys, compact separators, and non-ASCII preserved
        
    Raises:
        yaml.YAMLError: If the YAML contains unsafe tags
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    return json.dumps(
        data,
        sort_keys=True,
        separators=(',', ':'),
        ensure_ascii=False,
        cls=DateTimeEncoder
    )
