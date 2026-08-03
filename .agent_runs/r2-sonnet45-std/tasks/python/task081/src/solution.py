def diff_records(old, new, key):
    """
    Compare two lists of records and return differences.
    
    Args:
        old: List of dictionaries representing old records
        new: List of dictionaries representing new records
        key: String key to use for matching records
    
    Returns:
        Dictionary with keys "added", "removed", "changed"
    
    Raises:
        KeyError: If key is missing from any record
    """
    # Validate that all records have the key
    for record in old:
        if key not in record:
            raise KeyError(key)
    
    for record in new:
        if key not in record:
            raise KeyError(key)
    
    # Create dictionaries indexed by the key field
    old_dict = {record[key]: record for record in old}
    new_dict = {record[key]: record for record in new}
    
    # Find added records (in new but not in old)
    added = [record for record in new if record[key] not in old_dict]
    
    # Find removed records (in old but not in new)
    removed = [record for record in old if record[key] not in new_dict]
    
    # Find changed records (same key but different content)
    changed = []
    for record in new:
        record_key = record[key]
        if record_key in old_dict:
            # Key exists in both, check if content differs
            if record != old_dict[record_key]:
                changed.append(record)
    
    return {
        "added": added,
        "removed": removed,
        "changed": changed
    }
