# src/solution.py

def flatten_dict(d, sep="."):
    def _flatten(current_dict, parent_key=''):
        items = {}
        for k, v in current_dict.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                if v:  # Non-empty dict
                    items.update(_flatten(v, new_key))
                else:  # Empty dict
                    items[new_key] = {}
            else:
                if new_key in items:  # Check for key collision
                    raise ValueError(f"Key collision: {new_key}")
                items[new_key] = v
        return items

    return _flatten(d)
