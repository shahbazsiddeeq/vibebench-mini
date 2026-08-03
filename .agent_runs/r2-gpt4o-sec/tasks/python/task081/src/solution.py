# src/solution.py

def diff_records(old, new, key):
    if not isinstance(old, list) or not isinstance(new, list):
        raise TypeError("Both old and new must be lists of dictionaries.")
    
    old_dict = {}
    new_dict = {}
    
    for record in old:
        if not isinstance(record, dict):
            raise TypeError("Each record must be a dictionary.")
        if key not in record:
            raise KeyError(f"Key '{key}' missing from old record.")
        old_dict[record[key]] = record
    
    for record in new:
        if not isinstance(record, dict):
            raise TypeError("Each record must be a dictionary.")
        if key not in record:
            raise KeyError(f"Key '{key}' missing from new record.")
        new_dict[record[key]] = record
    
    added = [record for k, record in new_dict.items() if k not in old_dict]
    removed = [record for k, record in old_dict.items() if k not in new_dict]
    changed = [
        new_dict[k] for k in new_dict if k in old_dict and new_dict[k] != old_dict[k]
    ]
    
    return {
        "added": added,
        "removed": removed,
        "changed": changed
    }
