def diff_records(old, new, key):
    """
    Compares two lists of records (dictionaries) and identifies added, removed, and changed records.

    Args:
        old (list): The list of old records.
        new (list): The list of new records.
        key (str): The key to use for identifying records.

    Returns:
        dict: A dictionary with three keys:
              - "added": A list of records present in 'new' but not in 'old'.
              - "removed": A list of records present in 'old' but not in 'new'.
              - "changed": A list of records present in both, but with differing values
                           for other fields. The records in this list are from 'new'.

    Raises:
        KeyError: If the specified 'key' is missing from any record in either 'old' or 'new'.
    """
    old_map = {}
    for record in old:
        if key not in record:
            raise KeyError(f"Key '{key}' missing from old record: {record}")
        old_map[record[key]] = record

    new_map = {}
    for record in new:
        if key not in record:
            raise KeyError(f"Key '{key}' missing from new record: {record}")
        new_map[record[key]] = record

    added = []
    removed = []
    changed = []

    # Check for added and changed records
    for new_key, new_record in new_map.items():
        if new_key not in old_map:
            added.append(new_record)
        else:
            old_record = old_map[new_key]
            if new_record != old_record:
                changed.append(new_record)

    # Check for removed records
    for old_key, old_record in old_map.items():
        if old_key not in new_map:
            removed.append(old_record)

    return {
        "added": added,
        "removed": removed,
        "changed": changed,
    }
