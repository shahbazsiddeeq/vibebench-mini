# src/solution.py

def flatten(nested):
    result = []
    
    def _flatten(item):
        if isinstance(item, list):
            for sub_item in item:
                _flatten(sub_item)
        else:
            result.append(item)
    
    _flatten(nested)
    return result
