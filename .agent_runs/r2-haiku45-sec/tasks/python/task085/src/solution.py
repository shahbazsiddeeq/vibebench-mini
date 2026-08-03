import urllib.parse
from typing import Any, Dict, List, Union


def build_query(params: Dict[str, Any]) -> str:
    """
    Build a URL query string from a dictionary.
    
    - Keys are sorted alphabetically
    - List values become repeated keys
    - Values are URL-encoded using application/x-www-form-urlencoded format
    - Spaces are encoded as '+' (not '%20')
    
    Args:
        params: Dictionary with string keys and values that are strings, integers, or lists
        
    Returns:
        URL query string (empty string if params is empty)
    """
    if not params:
        return ""
    
    # Validate input
    if not isinstance(params, dict):
        raise TypeError("params must be a dictionary")
    
    # Build list of (key, value) pairs
    pairs: List[tuple] = []
    
    for key in sorted(params.keys()):
        # Validate key
        if not isinstance(key, str):
            raise TypeError(f"Dictionary keys must be strings, got {type(key).__name__}")
        
        value = params[key]
        
        # Handle list values
        if isinstance(value, list):
            for item in value:
                # Convert to string and validate
                str_item = _convert_to_string(item)
                pairs.append((key, str_item))
        else:
            # Convert to string and validate
            str_value = _convert_to_string(value)
            pairs.append((key, str_value))
    
    # URL encode using application/x-www-form-urlencoded format
    # quote_plus encodes spaces as '+' instead of '%20'
    encoded_pairs = [
        f"{urllib.parse.quote_plus(key)}={urllib.parse.quote_plus(value)}"
        for key, value in pairs
    ]
    
    return "&".join(encoded_pairs)


def _convert_to_string(value: Any) -> str:
    """
    Convert a value to string, validating it's a safe type.
    
    Args:
        value: Value to convert
        
    Returns:
        String representation of the value
        
    Raises:
        TypeError: If value is not a supported type
    """
    if isinstance(value, str):
        return value
    elif isinstance(value, int):
        return str(value)
    elif isinstance(value, float):
        return str(value)
    elif isinstance(value, bool):
        # Handle bool before int since bool is a subclass of int
        return str(value)
    elif value is None:
        return ""
    else:
        raise TypeError(
            f"Unsupported value type {type(value).__name__}. "
            f"Supported types: str, int, float, bool, None, or list of these"
        )
