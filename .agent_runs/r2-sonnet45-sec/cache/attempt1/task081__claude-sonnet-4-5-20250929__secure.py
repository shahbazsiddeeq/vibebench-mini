def diff_records(old, new, key):
    """
    Compare two lists of records and return differences.
    
    Args:
        old: List of dictionaries representing old records
        new: List of dictionaries representing new records
        key: String key field to match records by
        
    Returns:
        Dictionary with keys "added", "removed", "changed" containing lists of records
        
    Raises:
        KeyError: If key is missing from any record
    """
    # Validate inputs
    if not isinstance(old, list):
        raise TypeError("old must be a list")
    if not isinstance(new, list):
        raise TypeError("new must be a list")
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    
    # Build dictionaries indexed by key value for efficient lookup
    old_dict = {}
    new_dict = {}
    
    # Process old records
    for record in old:
        if not isinstance(record, dict):
            raise TypeError("All records must be dictionaries")
        if key not in record:
            raise KeyError(f"Key '{key}' not found in old record")
        key_value = record[key]
        old_dict[key_value] = record
    
    # Process new records
    for record in new:
        if not isinstance(record, dict):
            raise TypeError("All records must be dictionaries")
        if key not in record:
            raise KeyError(f"Key '{key}' not found in new record")
        key_value = record[key]
        new_dict[key_value] = record
    
    # Find added, removed, and changed records
    added = []
    removed = []
    changed = []
    
    # Find added and changed records
    for key_value, new_record in new_dict.items():
        if key_value not in old_dict:
            # Record is in new but not in old - it's added
            added.append(new_record)
        else:
            # Record exists in both - check if it changed
            old_record = old_dict[key_value]
            if old_record != new_record:
                # Record changed - return the new version
                changed.append(new_record)
    
    # Find removed records
    for key_value, old_record in old_dict.items():
        if key_value not in new_dict:
            # Record is in old but not in new - it's removed
            removed.append(old_record)
    
    return {
        "added": added,
        "removed": removed,
        "changed": changed
    }
