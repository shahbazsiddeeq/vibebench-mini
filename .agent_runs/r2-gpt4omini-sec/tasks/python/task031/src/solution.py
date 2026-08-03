# src/solution.py

def flatten(nested):
    if not isinstance(nested, list):
        raise ValueError("Input must be a list or a nested list.")
    
    flat_list = []
    
    def _flatten(item):
        if isinstance(item, list):
            for sub_item in item:
                _flatten(sub_item)
        else:
            flat_list.append(item)
    
    _flatten(nested)
    return flat_list
