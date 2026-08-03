def diff_records(old, new, key):
    """
    Compare two lists of records and return differences.
    
    Args:
        old: List of old records (dicts)
        new: List of new records (dicts)
        key: The key field to use for matching records
        
    Returns:
        Dict with "added", "removed", and "changed" keys
        
    Raises:
        KeyError: If the key is missing from any record
    """
    # Validate that key exists in all records
    for record in old:
        if key not in record:
            raise KeyError(key)
    for record in new:
        if key not in record:
            raise KeyError(key)
    
    # Create dictionaries indexed by key for easier lookup
    old_dict = {record[key]: record for record in old}
    new_dict = {record[key]: record for record in new}
    
    added = []
    removed = []
    changed = []
    
    # Find added records (in new but not in old)
    for key_val, record in new_dict.items():
        if key_val not in old_dict:
            added.append(record)
    
    # Find removed records (in old but not in new)
    for key_val, record in old_dict.items():
        if key_val not in new_dict:
            removed.append(record)
    
    # Find changed records (key matches but other fields differ)
    for key_val, new_record in new_dict.items():
        if key_val in old_dict:
            old_record = old_dict[key_val]
            if old_record != new_record:
                changed.append(new_record)
    
    return {
        "added": added,
        "removed": removed,
        "changed": changed
    }
