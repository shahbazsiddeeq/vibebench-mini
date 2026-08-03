# src/solution.py

def flatten_dict(d, sep="."):
    if not isinstance(d, dict):
        raise TypeError("Input must be a dictionary")
    if not isinstance(sep, str):
        raise TypeError("Separator must be a string")

    def _flatten(current_dict, parent_key=""):
        items = {}
        for k, v in current_dict.items():
            if not isinstance(k, str):
                raise ValueError("All keys must be strings")
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                if v:
                    items.update(_flatten(v, new_key))
                else:
                    if new_key in items:
                        raise ValueError(f"Collision detected for key: {new_key}")
                    items[new_key] = {}
            else:
                if new_key in items:
                    raise ValueError(f"Collision detected for key: {new_key}")
                items[new_key] = v
        return items

    return _flatten(d)
