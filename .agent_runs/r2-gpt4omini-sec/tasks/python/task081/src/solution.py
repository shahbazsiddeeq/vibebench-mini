# src/solution.py

def diff_records(old, new, key):
    # Validate inputs
    if not isinstance(old, list) or not isinstance(new, list):
        raise ValueError("Both old and new records must be lists.")
    
    if not isinstance(key, str):
        raise ValueError("Key must be a string.")

    old_dict = {record[key]: record for record in old}
    new_dict = {record[key]: record for record in new}

    # Check for missing keys in old records
    for record in old:
        if key not in record:
            raise KeyError(f"Key '{key}' is missing from old record: {record}")

    # Check for missing keys in new records
    for record in new:
        if key not in record:
            raise KeyError(f"Key '{key}' is missing from new record: {record}")

    added = [record for record in new if record[key] not in old_dict]
    removed = [record for record in old if record[key] not in new_dict]
    changed = [new_dict[k] for k in new_dict if k in old_dict and old_dict[k] != new_dict[k]]

    return {
        "added": added,
        "removed": removed,
        "changed": changed
    }
