def diff_records(old, new, key):
    """
    Compare two lists of records and return differences.
    
    Args:
        old: List of old records (dicts)
        new: List of new records (dicts)
        key: The key field to use for matching records
        
    Returns:
        Dict with "added", "removed", and "changed" keys containing lists of records
        
    Raises:
        KeyError: If the key is missing from any record
    """
    # Validate inputs
    if not isinstance(old, list):
        raise TypeError("old must be a list")
    if not isinstance(new, list):
        raise TypeError("new must be a list")
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    
    # Validate that key exists in all records
    for record in old:
        if not isinstance(record, dict):
            raise TypeError("All records must be dicts")
        if key not in record:
            raise KeyError(key)
    
    for record in new:
        if not isinstance(record, dict):
            raise TypeError("All records must be dicts")
        if key not in record:
            raise KeyError(key)
    
    # Build lookup dictionaries by key
    old_by_key = {record[key]: record for record in old}
    new_by_key = {record[key]: record for record in new}
    
    added = []
    removed = []
    changed = []
    
    # Find added records (in new but not in old)
    for key_value, record in new_by_key.items():
        if key_value not in old_by_key:
            added.append(record)
    
    # Find removed records (in old but not in new)
    for key_value, record in old_by_key.items():
        if key_value not in new_by_key:
            removed.append(record)
    
    # Find changed records (in both but with different values)
    for key_value, new_record in new_by_key.items():
        if key_value in old_by_key:
            old_record = old_by_key[key_value]
            if old_record != new_record:
                changed.append(new_record)
    
    return {
        "added": added,
        "removed": removed,
        "changed": changed
    }
