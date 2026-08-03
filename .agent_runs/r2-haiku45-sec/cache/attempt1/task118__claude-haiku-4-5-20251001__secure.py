"""
Flatten Dict module - safely flattens nested dictionaries into single-level dicts.
"""

from typing import Any, Dict, Union


def flatten_dict(d: Any, sep: str = ".") -> Dict[str, Any]:
    """
    Flatten a nested dictionary into a single-level dict with keys joined by sep.
    
    Args:
        d: The dictionary to flatten. Must be a dict.
        sep: The separator to use when joining keys. Must be a string.
    
    Returns:
        A flattened dictionary where nested keys are joined by sep.
        Empty dicts are preserved as leaf values.
    
    Raises:
        ValueError: If two different paths collapse to the same flattened key.
        TypeError: If d is not a dict or sep is not a string.
    """
    # Input validation
    if not isinstance(d, dict):
        raise TypeError("Input must be a dictionary")
    if not isinstance(sep, str):
        raise TypeError("Separator must be a string")
    
    # Handle empty top-level dict
    if not d:
        return {}
    
    result: Dict[str, Any] = {}
    seen_keys: Dict[str, str] = {}  # Track which path created each key
    
    def _flatten(obj: Any, prefix: str = "") -> None:
        """
        Recursively flatten the nested structure.
        
        Args:
            obj: Current object being processed.
            prefix: Current key path prefix.
        
        Raises:
            ValueError: If a key collision is detected.
        """
        if isinstance(obj, dict):
            # If dict is empty, treat it as a leaf value
            if not obj:
                if prefix in result:
                    raise ValueError(
                        f"Separator collision: key '{prefix}' already exists"
                    )
                result[prefix] = {}
                seen_keys[prefix] = prefix
            else:
                # Recursively process each key-value pair
                for key, value in obj.items():
                    # Validate key is a string to prevent injection
                    if not isinstance(key, str):
                        raise TypeError(f"Dictionary keys must be strings, got {type(key).__name__}")
                    
                    # Build the new prefix
                    new_prefix = f"{prefix}{sep}{key}" if prefix else key
                    
                    # Recursively flatten
                    _flatten(value, new_prefix)
        else:
            # Non-dict value is a leaf
            if prefix in result:
                raise ValueError(
                    f"Separator collision: key '{prefix}' already exists"
                )
            result[prefix] = obj
            seen_keys[prefix] = prefix
    
    _flatten(d)
    return result
