# src/solution.py

def flatten_dict(d, sep="."):
    if not isinstance(d, dict):
        raise ValueError("Input must be a dictionary.")
    
    if not isinstance(sep, str) or not sep:
        raise ValueError("Separator must be a non-empty string.")
    
    flat_dict = {}
    
    def _flatten(current_dict, parent_key=""):
        if not isinstance(current_dict, dict):
            raise ValueError("Nested structure must be a dictionary.")
        
        for key, value in current_dict.items():
            if not isinstance(key, str):
                raise ValueError("Dictionary keys must be strings.")
            
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            
            if isinstance(value, dict):
                if value:  # Only flatten if the dict is not empty
                    _flatten(value, new_key)
                else:  # Preserve empty dicts
                    flat_dict[new_key] = {}
            else:
                if new_key in flat_dict:
                    raise ValueError(f"Key collision detected: {new_key}")
                flat_dict[new_key] = value
    
    _flatten(d)
    return flat_dict
